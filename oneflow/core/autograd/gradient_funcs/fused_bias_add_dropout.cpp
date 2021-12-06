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
#include "oneflow/core/functional/functional.h"

namespace oneflow {
namespace one {

struct FusedBiasAddDropoutInterpState : public AutoGradCaptureState {
  bool input_requires_grad = true;
  bool bias_requires_grad = true;
  int32_t axis = 1;
  float scale = 1.0;
};

class FusedBiasAddDropout : public OpExprGradFunction<FusedBiasAddDropoutInterpState> {
 public:
  Maybe<void> Capture(FusedBiasAddDropoutInterpState* state, const TensorTuple& inputs,
                      const TensorTuple& outputs, const OpInterpCtx* ctx) const override;
  Maybe<void> Apply(const FusedBiasAddDropoutInterpState* state, const TensorTuple& out_grads,
                    TensorTuple* in_grads) const override;
};

Maybe<void> FusedBiasAddDropout::Capture(FusedBiasAddDropoutInterpState* state,
                                         const TensorTuple& inputs, const TensorTuple& outputs,
                                         const OpInterpCtx* ctx) const {
  CHECK_EQ_OR_RETURN(inputs.size(), 3);
  state->input_requires_grad = inputs.at(0)->requires_grad();  // input
  state->bias_requires_grad = inputs.at(1)->requires_grad();   // bias

  if (!state->input_requires_grad && !state->bias_requires_grad) { return Maybe<void>::Ok(); }
  auto* interp_ctx = dynamic_cast<const FusedBiasAddMaskScaleOpInterpCtx*>(ctx);
  state->scale = interp_ctx->scale;
  state->axis = interp_ctx->axis;

  state->SaveTensorForBackward(inputs.at(2));

  return Maybe<void>::Ok();
}

Maybe<void> FusedBiasAddDropout::Apply(const FusedBiasAddDropoutInterpState* state,
                                       const TensorTuple& out_grads, TensorTuple* in_grads) const {
  CHECK_EQ_OR_RETURN(out_grads.size(), 1);
  if (!state->input_requires_grad && !state->bias_requires_grad) { return Maybe<void>::Ok(); }

  // mask have no grad(reqiures_grad=False), but still take a place in in_grads
  in_grads->resize(3);

  const std::shared_ptr<oneflow::one::Tensor>& mask = state->SavedTensors().at(0);
  const std::shared_ptr<oneflow::one::Tensor>& dropout_grad =
      JUST(functional::DropoutGrad(out_grads.at(0), mask, state->scale));

  if (state->input_requires_grad) { in_grads->at(0) = dropout_grad; }

  const int64_t num_axes = out_grads.at(0)->shape()->NumAxes();
  if (state->bias_requires_grad) {
    std::vector<int32_t> reduce_axes_vec;
    reduce_axes_vec.reserve(num_axes);
    for (int i = 0; i < num_axes; ++i) {
      if (i != state->axis) { reduce_axes_vec.push_back(i); }
    }
    in_grads->at(1) = JUST(functional::ReduceSum(dropout_grad, reduce_axes_vec, false));
  }
  return Maybe<void>::Ok();
}

REGISTER_OP_EXPR_GRAD_FUNCTION("fused_bias_add_mask_scale", FusedBiasAddDropout);

}  // namespace one
}  // namespace oneflow
