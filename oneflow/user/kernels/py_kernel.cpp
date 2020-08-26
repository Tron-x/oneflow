
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
#include "oneflow/core/common/cpp_py.h"
#include "oneflow/core/framework/framework.h"

namespace oneflow {

void TensorToNdarray(const user_op::Tensor* tensor, PyObject* arg) {}

void NdarrayToTensor(PyObject* arg, user_op::Tensor* tensor) {}

void MakePyInputs(user_op::KernelComputeContext* ctx, PyObject* py_input) {
  size_t in_num = ctx->inputs().size();
  py_input = PyList_New(in_num);

  FOR_RANGE(size_t, i, 0, in_num) {
    PyObject* arg = nullptr;
    const std::string& arg_name = ctx->inputs().at(i).first;
    int32_t index = 0;
    TensorToNdarray(ctx->Tensor4ArgNameAndIndex(arg_name, index), arg);
    PyList_SetItem(py_input, i, arg);
  }
}

void GetPyOutputs(user_op::KernelComputeContext* ctx, PyObject* py_output) {
  size_t out_num = ctx->outputs().size();
  FOR_RANGE(size_t, i, 0, out_num) {}
}

template<typename T>
class PyKernel : public user_op::OpKernel {
 public:
  PyKernel() = default;
  ~PyKernel() = default;

  bool AlwaysComputeWhenAllOutputsEmpty() const override { return false; }

 private:
  void Compute(user_op::KernelComputeContext* ctx) const override {
    if (!PyEval_ThreadsInitialized()) { PyEval_InitThreads(); }
    PyGILState_STATE py_gil_st;
    py_gil_st = PyGILState_Ensure();
    if (PyArray_API == nullptr) { _import_array(); }

    PyRun_SimpleString("print('hello')");

    PyObject *py_name, *py_module, *py_func;
    PyObject *py_inputs, *py_outputs;

    // load python kernel
    py_name = PyUnicode_DecodeFSDefault("pyk_sigmoid");
    // Error checking of pName left out
    py_module = PyImport_Import(py_name);
    Py_DECREF(py_name);
    if (py_module == nullptr) { PyErr_Print(); }

    // get forward func
    py_func = PyObject_GetAttrString(py_module, "forward");
    if (py_func == nullptr || !PyCallable_Check(py_func)) {
      Py_DECREF(py_module);
      PyErr_Print();
    }

    // input
    MakePyInputs(ctx, py_inputs);

    // call func
    py_outputs = PyObject_CallObject(py_func, py_inputs);
    Py_DECREF(py_inputs);

    // output
    GetPyOutputs(ctx, py_outputs);

    Py_DECREF(py_outputs);
    Py_XDECREF(py_func);
    Py_DECREF(py_module);

    PyGILState_Release(py_gil_st);
  }
};  // namespace oneflow

#define REGISTER_PY_KERNEL(cpp_type, dtype)                                     \
  REGISTER_USER_KERNEL("py").SetCreateFn<PyKernel<cpp_type>>().SetIsMatchedHob( \
      (user_op::HobDeviceTag() == "cpu") & (user_op::HobDataType("in", 0) == dtype));

OF_PP_FOR_EACH_TUPLE(REGISTER_PY_KERNEL, ARITHMETIC_DATA_TYPE_SEQ);

template<typename T>
class PyGradKernel final : public user_op::OpKernel {
 public:
  PyGradKernel() = default;
  ~PyGradKernel() = default;

 private:
  void Compute(user_op::KernelComputeContext* ctx) const override {
    const user_op::Tensor* x_blob = ctx->Tensor4ArgNameAndIndex("x", 0);
    const user_op::Tensor* y_blob = ctx->Tensor4ArgNameAndIndex("y", 0);
    const user_op::Tensor* dy_blob = ctx->Tensor4ArgNameAndIndex("dy", 0);
    user_op::Tensor* dx_blob = ctx->Tensor4ArgNameAndIndex("dx", 0);
    // TODO(strint) : compute backward with py
  }
  bool AlwaysComputeWhenAllOutputsEmpty() const override { return false; }
};

#define REGISTER_PY_GRAD_KERNEL(cpp_type, dtype)                                         \
  REGISTER_USER_KERNEL("py_grad").SetCreateFn<PyGradKernel<cpp_type>>().SetIsMatchedHob( \
      (user_op::HobDeviceTag() == "cpu") & (user_op::HobDataType("dx", 0) == dtype));

OF_PP_FOR_EACH_TUPLE(REGISTER_PY_GRAD_KERNEL, ARITHMETIC_DATA_TYPE_SEQ);

}  // namespace oneflow
