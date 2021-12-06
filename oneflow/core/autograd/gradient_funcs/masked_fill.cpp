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
#include "oneflow/core/framework/op_builder.h"
#include "oneflow/core/framework/op_interpreter/op_interpreter_util.h"
#include "oneflow/core/functional/functional.h"

namespace oneflow {
namespace one {

struct MaskedFillCaptureState : public AutoGradCaptureState {
  bool requires_grad = true;
};

class MaskedFill : public OpExprGradFunction<MaskedFillCaptureState> {
 public:
  Maybe<void> Capture(MaskedFillCaptureState* state, const TensorTuple& inputs,
                      const TensorTuple& outputs, const OpInterpCtx* ctx) const override {
    state->requires_grad = inputs.at(0)->requires_grad();
    if (!state->requires_grad) { return Maybe<void>::Ok(); }

    state->SaveTensorForBackward(inputs.at(0));
    state->SaveTensorForBackward(inputs.at(1));
    return Maybe<void>::Ok();
  }
  Maybe<void> Apply(const MaskedFillCaptureState* state, const TensorTuple& out_grads,
                    TensorTuple* in_grads) const override {
    if (!state->requires_grad) { return Maybe<void>::Ok(); }
    CHECK_EQ_OR_RETURN(out_grads.size(), 1);
    const std::shared_ptr<oneflow::one::Tensor>& x = state->SavedTensors().at(0);
    const std::shared_ptr<oneflow::one::Tensor>& mask = state->SavedTensors().at(1);

    std::shared_ptr<oneflow::one::Tensor> zero_out = JUST(functional::ZerosLike(x));
    in_grads->resize(2);
    in_grads->at(0) = JUST(functional::Where(mask, zero_out, out_grads.at(0)));
    return Maybe<void>::Ok();
  }
};

REGISTER_OP_EXPR_GRAD_FUNCTION("masked_fill", MaskedFill);

}  // namespace one
}  // namespace oneflow
