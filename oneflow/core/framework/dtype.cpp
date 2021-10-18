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
#include "half.hpp"
#include "oneflow/core/common/util.h"
#include "oneflow/core/common/switch_func.h"
#include "oneflow/core/common/container_util.h"
#include "oneflow/core/common/data_type_seq.h"
#include "oneflow/core/common/protobuf.h"
#include "oneflow/core/framework/dtype.h"
#include "oneflow/core/framework/device_register_cpu.h"

namespace oneflow {

namespace {

template<typename T>
std::size_t GetDataTypeBytes() {
  return sizeof(T);
}

#define MAKE_DATA_TYPE_BYTES_SWITCH_ENTRY(func_name, T) func_name<T>
DEFINE_STATIC_SWITCH_FUNC(std::size_t, GetDataTypeBytes, MAKE_DATA_TYPE_BYTES_SWITCH_ENTRY,
                          MAKE_DATA_TYPE_CTRV_SEQ(POD_DATA_TYPE_SEQ FLOAT16_DATA_TYPE_SEQ));

class DTypeMeta final {
 public:
  DTypeMeta(const std::string& name, bool is_signed, bool is_floating_point, bool is_complex)
      : name_(name),
        is_signed_(is_signed),
        is_floating_point_(is_floating_point),
        is_complex_(is_complex) {}
  DTypeMeta(const DTypeMeta&) = default;
  DTypeMeta(DTypeMeta&) = default;
  ~DTypeMeta() = default;

  const std::string& name() const { return name_; }
  bool is_signed() const { return is_signed_; }
  bool is_floating_point() const { return is_floating_point_; }
  bool is_complex() const { return is_complex_; }

 private:
  const std::string name_;
  const bool is_signed_;
  const bool is_floating_point_;
  const bool is_complex_;
};

Maybe<const DTypeMeta&> DTypeMeta4DataType(DataType data_type) {
  static HashMap<DataType, DTypeMeta> data_type2dtype_meta{
      {DataType::kInvalidDataType, DTypeMeta("oneflow.invalid_data_type", false, false, false)},
      {DataType::kChar, DTypeMeta("oneflow.char", false, false, false)},
      {DataType::kFloat16, DTypeMeta("oneflow.float16", true, true, false)},
      {DataType::kFloat, DTypeMeta("oneflow.float32", true, true, false)},
      {DataType::kDouble, DTypeMeta("oneflow.float64", true, true, false)},
      {DataType::kInt8, DTypeMeta("oneflow.int8", true, false, false)},
      {DataType::kInt32, DTypeMeta("oneflow.int32", true, false, false)},
      {DataType::kInt64, DTypeMeta("oneflow.int64", true, false, false)},
      {DataType::kUInt8, DTypeMeta("oneflow.uint8", false, false, false)},
      {DataType::kOFRecord, DTypeMeta("oneflow.of_record", false, false, false)},
      {DataType::kTensorBuffer, DTypeMeta("oneflow.tensor_buffer", false, false, false)},
      {DataType::kBFloat16, DTypeMeta("oneflow.bfloat16", true, true, false)},
  };
  return MapAt(data_type2dtype_meta, data_type);
};

}  // namespace

Maybe<const Symbol<DType>&> DType::Get(DataType data_type) {
  static HashMap<DataType, const Symbol<DType>> data_type2dtype{
#define MAKE_ENTRY(data_type) {OF_PP_CAT(DataType::k, data_type), data_type()},
      OF_PP_FOR_EACH_TUPLE(MAKE_ENTRY, DTYPE_SEQ)
#undef MAKE_ENTRY
  };
  return MapAt(data_type2dtype, data_type);
}

Maybe<size_t> DType::bytes() const {
  // DataType::OFRecord and DataType::TensorBuffer don't have fixed byte size
  if (data_type() == DataType::kInvalidDataType || data_type() == DataType::kOFRecord
      || data_type() == DataType::kTensorBuffer) {
    OF_UNIMPLEMENTED();
  }
  return SwitchGetDataTypeBytes(SwitchCase(data_type()));
}

bool DType::is_signed() const { return CHECK_JUST(DTypeMeta4DataType(data_type_)).is_signed(); }

bool DType::is_complex() const { return CHECK_JUST(DTypeMeta4DataType(data_type_)).is_complex(); }

/*
  The order of datatype is:
  0    1    2    3    4    5    6    7    8    9    10   11
  iv   c1   f4   f8   i1   i4   i8   u1   re   f2   bu   bf
  The priority order of datatype is:
  0    1    2    3    4    5    6    7    8    9    10   11
  iv < u1 < c1 < i1 < i4 < i8 < f2 < f4 < f8 < bf < re < bu.
*/
const int DType::priority_order[DataType::kMaxDataType] = {0,  /*kInvalid*/
                                                           2,  /*kChar*/
                                                           7,  /*kFloat32*/
                                                           8,  /*kDouble*/
                                                           3,  /*kInt8*/
                                                           4,  /*kInt32*/
                                                           5,  /*kInt64*/
                                                           1,  /*kUInt8*/
                                                           10, /*kOFRecord*/
                                                           6,  /*kFloat16*/
                                                           11, /*kTensorBuffer*/
                                                           9 /*kBFloat16*/};

bool DType::is_floating_point() const {
  return CHECK_JUST(DTypeMeta4DataType(data_type_)).is_floating_point();
}

const std::string& DType::name() const { return CHECK_JUST(DTypeMeta4DataType(data_type_)).name(); }

#define DEFINE_GET_DATA_TYPE_FUNCTION(data_type)                                   \
  const Symbol<DType>& DType::data_type() {                                        \
    static const auto& dtype = SymbolOf(DType(OF_PP_CAT(DataType::k, data_type))); \
    return dtype;                                                                  \
  }
OF_PP_FOR_EACH_TUPLE(DEFINE_GET_DATA_TYPE_FUNCTION, DTYPE_SEQ)
#undef DEFINE_GET_DATA_TYPE_FUNCTION

Symbol<DType> promoteTypes(const Symbol<DType> a, const Symbol<DType> b) {
  const Symbol<DType> iv = CHECK_JUST(DType::Get(DataType::kInvalidDataType));
  const Symbol<DType> c1 = CHECK_JUST(DType::Get(DataType::kChar));
  const Symbol<DType> f4 = CHECK_JUST(DType::Get(DataType::kFloat));
  const Symbol<DType> f8 = CHECK_JUST(DType::Get(DataType::kDouble));
  const Symbol<DType> i1 = CHECK_JUST(DType::Get(DataType::kInt8));
  const Symbol<DType> i4 = CHECK_JUST(DType::Get(DataType::kInt32));
  const Symbol<DType> i8 = CHECK_JUST(DType::Get(DataType::kInt64));
  const Symbol<DType> u1 = CHECK_JUST(DType::Get(DataType::kUInt8));
  const Symbol<DType> re = CHECK_JUST(DType::Get(DataType::kOFRecord));
  const Symbol<DType> f2 = CHECK_JUST(DType::Get(DataType::kFloat16));
  const Symbol<DType> bu = CHECK_JUST(DType::Get(DataType::kTensorBuffer));
  const Symbol<DType> bf = CHECK_JUST(DType::Get(DataType::kBFloat16));

  /* It is consistent with data_type.proto(except kInvalidDataType, kOFRecord and kTensorBuffer)
    kInvalidDataType = 0;
    kChar = 1;
    kFloat = 2;
    kDouble = 3;
    kInt8 = 4;
    kInt32 = 5;
    kInt64 = 6;
    kUInt8 = 7;
    kOFRecord = 8;
    kFloat16 = 9;
    kTensorBuffer = 10;
    kBFloat16 = 11;

    The priority order of datatype is:
    iv < u1 < c1 < i1 < i4 < i8 < f2 < f4 < f8 < bf < re < bu.

    The new DataType should be add in the end of proto, and the Loopup table should be maintained as
    right priority (author:zhengzekang).
  */
  static const Symbol<DType> _promoteTypesLookup[DataType::kMaxDataType][DataType::kMaxDataType] = {
      /*        iv  c1  f4  f8  i1  i4  i8  u1  re  f2  bu  bf */
      /* iv */ {iv, c1, f4, f8, i1, i4, i8, u1, re, f2, bu, bf},
      /* c1 */ {c1, c1, f4, f8, i1, i4, i8, c1, re, f2, bu, bf},
      /* f4 */ {f4, f4, f4, f8, f4, f4, f4, f4, re, f4, bu, bf},
      /* f8 */ {f8, f8, f8, f8, f8, f8, f8, f8, re, f8, bu, bf},
      /* i1 */ {i1, i1, f4, f8, i1, i4, i8, i1, re, f2, bu, bf},
      /* i4 */ {i4, i4, f4, f8, i4, i4, i8, i4, re, f2, bu, bf},
      /* i8 */ {i8, i8, f4, f8, i8, i8, i8, i8, re, f2, bu, bf},
      /* u1 */ {u1, c1, f4, f8, i1, i4, i8, u1, re, f2, bu, bf},
      /* re */ {re, re, re, re, re, re, re, re, re, re, bu, re},
      /* f2 */ {f2, f2, f4, f8, f2, f2, f2, f2, re, f2, bu, bf},
      /* bu */ {bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu},
      /* bf */ {bf, bf, bf, bf, bf, bf, bf, bf, re, bf, bu, bf},
  };

  return _promoteTypesLookup[static_cast<int>(a->data_type())][static_cast<int>(b->data_type())];
}

}  // namespace oneflow