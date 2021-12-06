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

namespace oneflow {
namespace one {

struct FakeQuantizationCaptureState : public AutoGradCaptureState {
  bool requires_grad;
};

class FakeQuantization : public OpExprGradFunction<FakeQuantizationCaptureState> {
 public:
  Maybe<void> Capture(FakeQuantizationCaptureState* state, const TensorTuple& inputs,
                      const TensorTuple& outputs, const OpInterpCtx* ctx) const override {
    CHECK_EQ_OR_RETURN(inputs.size(), 3);
    state->requires_grad = inputs.at(0)->requires_grad();
    return Maybe<void>::Ok();
  }

  Maybe<void> Apply(const FakeQuantizationCaptureState* state, const TensorTuple& out_grads,
                    TensorTuple* in_grads) const override {
    CHECK_EQ_OR_RETURN(out_grads.size(), 1);
    in_grads->resize(3);
    if (state->requires_grad) { in_grads->at(0) = out_grads.at(0); }
    return Maybe<void>::Ok();
  }
};

REGISTER_OP_EXPR_GRAD_FUNCTION("fake_quantization", FakeQuantization);

}  // namespace one
}  // namespace oneflow
