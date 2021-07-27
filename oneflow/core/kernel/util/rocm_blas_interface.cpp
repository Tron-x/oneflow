/*
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#if defined(WITH_HIP)

#include "oneflow/core/kernel/util/cuda_blas_interface.h"
#include "oneflow/core/device/hip_util.hip.h"
#include "oneflow/core/register/blob.h"
#include "oneflow/core/kernel/util/rocm_half_util.h"

namespace oneflow {

namespace {

hipblasOperation_t CblasTrans2CublasTrans(CBLAS_TRANSPOSE trans) {
  hipblasOperation_t hipblas_trans;
  if (trans == CBLAS_TRANSPOSE::CblasNoTrans) {
    hipblas_trans = hipblasOperation_t::HIPBLAS_OP_N ;
  } else if (trans == CBLAS_TRANSPOSE::CblasTrans) {
    hipblas_trans = hipblasOperation_t::HIPBLAS_OP_T ;
  } else if (trans == CBLAS_TRANSPOSE::CblasConjTrans) {
    hipblas_trans = hipblasOperation_t::HIPBLAS_OP_C ;
  } else {
    // do nothing
  }
  return hipblas_trans;
}

std::tuple<int, int, int, hipblasOperation_t, hipblasOperation_t> PrepareToCallCublasGemm(
    enum CBLAS_TRANSPOSE trans_a, enum CBLAS_TRANSPOSE trans_b, const int m, const int n,
    const int k) {
  int lda = (trans_a == CblasNoTrans) ? k : m;
  int ldb = (trans_b == CblasNoTrans) ? n : k;
  int ldc = n;
  hipblasOperation_t cublas_trans_a = CblasTrans2CublasTrans(trans_a);
  hipblasOperation_t cublas_trans_b = CblasTrans2CublasTrans(trans_b);
  return std::make_tuple(lda, ldb, ldc, cublas_trans_a, cublas_trans_b);
}

template<typename T>
void Gemm(DeviceCtx* ctx, const enum CBLAS_ORDER order, enum CBLAS_TRANSPOSE trans_a,
          enum CBLAS_TRANSPOSE trans_b, const int m, const int n, const int k, const double alpha,
          const T* a, const T* b, const double beta, T* c) {
  int lda, ldb, ldc;
  hipblasOperation_t cublas_trans_a, cublas_trans_b;
  std::tie(lda, ldb, ldc, cublas_trans_a, cublas_trans_b) =
      PrepareToCallCublasGemm(trans_a, trans_b, m, n, k);

  hipblasHandle_t handle;
  if (std::is_same<T, half>::value) {
    handle = ctx->hipblas_tensor_op_math_handle();
  } else {
    handle = ctx->hipblas_pmh_handle();
  }
  const T alpha_val = static_cast<T>(alpha);
  const T beta_val = static_cast<T>(beta);
  hipblasSgemm(handle, cublas_trans_b, cublas_trans_a, n, m, k, &alpha_val, b, ldb, a, lda,
                 &beta_val, c, ldc);
}

template<>
void Gemm(DeviceCtx* ctx, const enum CBLAS_ORDER order, enum CBLAS_TRANSPOSE trans_a,
          enum CBLAS_TRANSPOSE trans_b, const int m, const int n, const int k, const double alpha,
          const double* a, const double* b, const double beta, double* c) {
  int lda, ldb, ldc;
  hipblasOperation_t cublas_trans_a, cublas_trans_b;
  std::tie(lda, ldb, ldc, cublas_trans_a, cublas_trans_b) =
      PrepareToCallCublasGemm(trans_a, trans_b, m, n, k);

  hipblasHandle_t handle;
  handle = ctx->hipblas_pmh_handle();
  const double alpha_val = static_cast<double>(alpha);
  const double beta_val = static_cast<double>(beta);
  hipblasDgemm(handle, cublas_trans_b, cublas_trans_a, n, m, k, &alpha_val, b, ldb, a, lda,
                 &beta_val, c, ldc);
}

template<>
void Gemm(DeviceCtx* ctx, const enum CBLAS_ORDER order, enum CBLAS_TRANSPOSE trans_a,
          enum CBLAS_TRANSPOSE trans_b, const int m, const int n, const int k, const double alpha,
          const half* a, const half* b, const double beta, half* c) {
  const float alpha_f = static_cast<float>(alpha);
  const float beta_f = static_cast<float>(beta);
  int lda, ldb, ldc;
  hipblasOperation_t cublas_trans_a, cublas_trans_b;
  std::tie(lda, ldb, ldc, cublas_trans_a, cublas_trans_b) =
      PrepareToCallCublasGemm(trans_a, trans_b, m, n, k);
    OF_HIPBLAS_CHECK(hipblasGemmEx(ctx->hipblas_tensor_op_math_handle(), cublas_trans_b,
                                 cublas_trans_a, n, m, k, &alpha_f, b, HIPBLAS_R_16F, ldb, a,
                                 HIPBLAS_R_16F, lda, &beta_f, c, HIPBLAS_R_16F, ldc, HIPBLAS_R_32F,
                                 HIPBLAS_GEMM_DEFAULT));
}

std::tuple<int, int, int> CalcMNKForGemm(enum CBLAS_TRANSPOSE trans_a, const Blob* a,
                                         const Blob* c) {
  const auto& a_shape = a->shape_view();
  const auto& c_shape = c->shape_view();
  int m = c_shape.At(0);
  int n = c_shape.Count(1);
  int k = (trans_a == CblasNoTrans) ? a_shape.Count(1) : a_shape.At(0);
  return std::make_tuple(m, n, k);
}

std::tuple<int, int, int, int, int, int, hipblasOperation_t, hipblasOperation_t>
PrepareToCallBatchedGemm(const enum CBLAS_TRANSPOSE trans_a, const enum CBLAS_TRANSPOSE trans_b,
                         int batch_size, int m, int n, int k) {
  const int a_stride = m * k;
  const int b_stride = k * n;
  const int c_stride = m * n;
  const int lda = (trans_a == CblasNoTrans) ? k : m;
  const int ldb = (trans_b == CblasNoTrans) ? n : k;
  const int ldc = n;
  hipblasOperation_t cublas_trans_a = CblasTrans2CublasTrans(trans_a);
  hipblasOperation_t cublas_trans_b = CblasTrans2CublasTrans(trans_b);
  return std::make_tuple(a_stride, b_stride, c_stride, lda, ldb, ldc, cublas_trans_a,
                         cublas_trans_b);
}

template<typename T>
hipblasDatatype_t GetCudaDataType4BatchedGemm() {
  return HipDataType<T>::value;
}

template<>
hipblasDatatype_t GetCudaDataType4BatchedGemm<half>() {
  return HIPBLAS_R_16F;
}

template<typename T>
void BatchedGemmImpl(DeviceCtx* ctx, const enum CBLAS_ORDER order,
                     const enum CBLAS_TRANSPOSE trans_a, const enum CBLAS_TRANSPOSE trans_b,
                     int batch_size, int m, int n, int k, const double alpha, const T* a,
                     const T* b, const double beta, T* c) {
  int a_stride, b_stride, c_stride;
  int lda, ldb, ldc;
  const T alpha_val = static_cast<T>(alpha);
  const T beta_val = static_cast<T>(beta);
  hipblasOperation_t cublas_trans_a, cublas_trans_b;
  std::tie(a_stride, b_stride, c_stride, lda, ldb, ldc, cublas_trans_a, cublas_trans_b) =
      PrepareToCallBatchedGemm(trans_a, trans_b, batch_size, m, n, k);

    hipblasDatatype_t data_type = GetCudaDataType4BatchedGemm<T>();
    OF_HIPBLAS_CHECK(hipblasGemmStridedBatchedEx(
        ctx->hipblas_pmh_handle(), cublas_trans_b, cublas_trans_a, n, m, k,
        reinterpret_cast<const void*>(&alpha_val), reinterpret_cast<const void*>(b), data_type, ldb,
        b_stride, reinterpret_cast<const void*>(a), data_type, lda, a_stride,
        reinterpret_cast<const void*>(&beta_val), reinterpret_cast<void*>(c), data_type, ldc,
        c_stride, batch_size, data_type, HIPBLAS_GEMM_DEFAULT));
}

template<>
void BatchedGemmImpl(DeviceCtx* ctx, const enum CBLAS_ORDER order,
                     const enum CBLAS_TRANSPOSE trans_a, const enum CBLAS_TRANSPOSE trans_b,
                     int batch_size, int m, int n, int k, const double alpha, const half* a,
                     const half* b, const double beta, half* c) {
  int a_stride, b_stride, c_stride;
  int lda, ldb, ldc;
  hipblasOperation_t cublas_trans_a, cublas_trans_b;
  std::tie(a_stride, b_stride, c_stride, lda, ldb, ldc, cublas_trans_a, cublas_trans_b) =
      PrepareToCallBatchedGemm(trans_a, trans_b, batch_size, m, n, k);

//   if (GetCudaSmVersion() >= 500) {
    const float alpha_f = static_cast<float>(alpha);
    const float beta_f = static_cast<float>(beta);
// #if CUDA_VERSION >= 11000
    hipblasGemmAlgo_t algo = HIPBLAS_GEMM_DEFAULT;
// #else
//     cublasGemmAlgo_t algo = CUBLAS_GEMM_DFALT_TENSOR_OP;
// #endif
    OF_HIPBLAS_CHECK(hipblasGemmStridedBatchedEx(
        ctx->hipblas_tensor_op_math_handle(), cublas_trans_b, cublas_trans_a, n, m, k, &alpha_f,
        reinterpret_cast<const void*>(b), HIPBLAS_R_16F, ldb, b_stride,
        reinterpret_cast<const void*>(a), HIPBLAS_R_16F, lda, a_stride, &beta_f,
        reinterpret_cast<void*>(c), HIPBLAS_R_16F, ldc, c_stride, batch_size, HIPBLAS_R_32F, algo));
//   } else {
//     const half alpha_h = static_cast<half>(alpha);
//     const half beta_h = static_cast<half>(beta);
//     cublas_gemmStridedBatched<half>(ctx->cublas_tensor_op_math_handle(), cublas_trans_b,
//                                     cublas_trans_a, n, m, k, &alpha_h, b, ldb, b_stride, a, lda,
//                                     a_stride, &beta_h, c, ldc, c_stride, batch_size);
//   }
}

__global__ void AxpyHalfGpu(const int n, const half alpha, const half* x, const int incx, half* y,
                            const int incy) {
// #if __CUDA_ARCH__ >= 530 || !defined(__CUDA_ARCH__)
  HIP_1D_KERNEL_LOOP(i, n) { y[i * incy] = __hfma(alpha, x[i * incx], y[i * incy]); }
// #else
//   HALF_CHECK_FAILED;
// #endif  // __CUDA_ARCH__ >= 530 || !defined(__CUDA_ARCH__)
}

__global__ void AxpyHalf2Gpu(const int n, const half alpha, const half* x, half* y) {
  const int h2_n = n / 2;
  const auto* x_h2 = reinterpret_cast<const half2*>(x);
  auto* y_h2 = reinterpret_cast<half2*>(y);
  half2 alpha_h2 = __half2half2(alpha);
  HIP_1D_KERNEL_LOOP(i, h2_n) { y_h2[i] = __hfma2(alpha_h2, x_h2[i], y_h2[i]); }
  if (n % 2 != 0 && blockIdx.x == 0 && threadIdx.x == 0) {
    const int last_idx = n - 1;
    y[last_idx] = __hfma(alpha, x[last_idx], y[last_idx]);
  }
}

}  // namespace

void BlasIf<DeviceType::kGPU>::OFGemm(DeviceCtx* ctx, enum CBLAS_TRANSPOSE trans_a,
                                      enum CBLAS_TRANSPOSE trans_b, const int m, const int n,
                                      const int k, const double alpha, const float* a,
                                      const float* b, const double beta, float* c) {
  Gemm<float>(ctx, CblasRowMajor, trans_a, trans_b, m, n, k, alpha, a, b, beta, c);
}
void BlasIf<DeviceType::kGPU>::OFGemm(DeviceCtx* ctx, enum CBLAS_TRANSPOSE trans_a,
                                      enum CBLAS_TRANSPOSE trans_b, const int m, const int n,
                                      const int k, const double alpha, const double* a,
                                      const double* b, const double beta, double* c) {
  Gemm<double>(ctx, CblasRowMajor, trans_a, trans_b, m, n, k, alpha, a, b, beta, c);
}
void BlasIf<DeviceType::kGPU>::OFGemm(DeviceCtx* ctx, enum CBLAS_TRANSPOSE trans_a,
                                      enum CBLAS_TRANSPOSE trans_b, const int m, const int n,
                                      const int k, const double alpha, const float16* a,
                                      const float16* b, const double beta, float16* c) {
  Gemm<half>(ctx, CblasRowMajor, trans_a, trans_b, m, n, k, alpha, reinterpret_cast<const half*>(a),
             reinterpret_cast<const half*>(b), beta, reinterpret_cast<half*>(c));
}

void BlasIf<DeviceType::kGPU>::OFBatchedGemm(DeviceCtx* ctx, enum CBLAS_TRANSPOSE trans_a,
                                             enum CBLAS_TRANSPOSE trans_b, const int batch_size,
                                             const int m, const int n, const int k,
                                             const double alpha, const float* a, const float* b,
                                             const double beta, float* c) {
  BatchedGemmImpl<float>(ctx, CblasRowMajor, trans_a, trans_b, batch_size, m, n, k, alpha, a, b,
                         beta, c);
}
void BlasIf<DeviceType::kGPU>::OFBatchedGemm(DeviceCtx* ctx, enum CBLAS_TRANSPOSE trans_a,
                                             enum CBLAS_TRANSPOSE trans_b, const int batch_size,
                                             const int m, const int n, const int k,
                                             const double alpha, const double* a, const double* b,
                                             const double beta, double* c) {
  BatchedGemmImpl<double>(ctx, CblasRowMajor, trans_a, trans_b, batch_size, m, n, k, alpha, a, b,
                          beta, c);
}
void BlasIf<DeviceType::kGPU>::OFBatchedGemm(DeviceCtx* ctx, enum CBLAS_TRANSPOSE trans_a,
                                             enum CBLAS_TRANSPOSE trans_b, const int batch_size,
                                             const int m, const int n, const int k,
                                             const double alpha, const float16* a, const float16* b,
                                             const double beta, float16* c) {
  BatchedGemmImpl<half>(ctx, CblasRowMajor, trans_a, trans_b, batch_size, m, n, k, alpha,
                        reinterpret_cast<const half*>(a), reinterpret_cast<const half*>(b), beta,
                        reinterpret_cast<half*>(c));
}

void BlasIf<DeviceType::kGPU>::Axpy(DeviceCtx* ctx, const int n, const float alpha, const float* x,
                                    const int incx, float* y, const int incy) {
  hipblasSaxpy(ctx->hipblas_pmh_handle(), n, &alpha, x, incx, y, incy);
}

void BlasIf<DeviceType::kGPU>::Axpy(DeviceCtx* ctx, const int n, const double alpha,
                                    const double* x, const int incx, double* y, const int incy) {
  hipblasDaxpy(ctx->hipblas_pmh_handle(), n, &alpha, x, incx, y, incy);
}

void BlasIf<DeviceType::kGPU>::Axpy(DeviceCtx* ctx, const int n, const float16 alpha,
                                    const float16* x, const int incx, float16* y, const int incy) {
  if (incx == 1 && incy == 1) {
    AxpyHalf2Gpu<<<BlocksNum4ThreadsNum(n / 2), kHipThreadsNumPerBlock, 0, ctx->rocm_stream()>>>(
        n, float16_2half(alpha), reinterpret_cast<const half*>(x), reinterpret_cast<half*>(y));
  } else {
    AxpyHalfGpu<<<BlocksNum4ThreadsNum(n), kHipThreadsNumPerBlock, 0, ctx->rocm_stream()>>>(
        n, float16_2half(alpha), reinterpret_cast<const half*>(x), incx, reinterpret_cast<half*>(y),
        incy);
  }
}

}  // namespace oneflow

#endif
