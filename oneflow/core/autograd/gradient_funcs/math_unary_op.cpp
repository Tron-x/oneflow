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

#include "oneflow/core/framework/op_expr_grad_function.h"
#include "oneflow/core/framework/op_interpreter/op_interpreter_util.h"
#include "oneflow/user/ops/math_unary_elementwise_seq.h"
#include "oneflow/core/functional/functional.h"

namespace oneflow {
namespace one {

struct UnaryMathCaptureState : public AutoGradCaptureState {
  bool x_requires_grad;
};

typedef Maybe<one::Tensor> (*UnaryBwFunc)(const std::shared_ptr<one::Tensor>&,
                                          const std::shared_ptr<one::Tensor>&);

template<UnaryBwFunc BwFunc>
class UnaryMathOp : public OpExprGradFunction<UnaryMathCaptureState> {
  Maybe<void> Capture(UnaryMathCaptureState* state, const TensorTuple& inputs,
                      const TensorTuple& outputs, const OpInterpCtx* ctx) const override {
    state->x_requires_grad = inputs.at(0)->requires_grad();
    state->SaveTensorForBackward(inputs.at(0));
    return Maybe<void>::Ok();
  }

  Maybe<void> Apply(const UnaryMathCaptureState* state, const TensorTuple& out_grads,
                    TensorTuple* in_grads) const override {
    if (!state->x_requires_grad) { return Maybe<void>::Ok(); }
    const auto& x = state->SavedTensors().at(0);
    in_grads->at(0) = JUST(BwFunc(x, out_grads.at(0)));
    return Maybe<void>::Ok();
  }
};

#define INSTANTIAT_AND_REGISTER_UNARY_MATHOP_CLASS(op_type_name, op_cls)     \
  class op_cls##Cls final : public UnaryMathOp<functional::op_cls##Grad> {}; \
  REGISTER_OP_EXPR_GRAD_FUNCTION(op_type_name, op_cls##Cls);

OF_PP_FOR_EACH_TUPLE(INSTANTIAT_AND_REGISTER_UNARY_MATHOP_CLASS, MATH_UNARY_ELEMENTWISE_FUNC_SEQ);

#undef INSTANTIAT_AND_REGISTER_UNARY_MATHOP_CLASS
}  // namespace one
}  // namespace oneflow
