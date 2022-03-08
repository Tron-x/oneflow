"""
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
"""
import unittest
import numpy as np
import oneflow as flow
from collections import OrderedDict
from oneflow.test_utils.automated_test_util import *
from oneflow.nn.modules import min_max_observer
from oneflow.test_utils.test_util import GenArgList
from oneflow.test.modules.test_min_max_observer import _check_min_max_observer


def _run_test_min_max_observer(
    test_case,
    placement,
    sbp,
    device_type,
    weight_shape,
    quantization_bit,
    quantization_scheme,
    quantization_formula,
    per_layer_quantization,
):
    weight = random_tensor(
        len(weight_shape), *weight_shape, low=-0.5, high=0.5
    ).to_global(placement, sbp)
    of_weight = weight.oneflow
    np_weight = of_weight.numpy()

    min_max_observer = flow.nn.MinMaxObserver(
        quantization_formula=quantization_formula,
        quantization_bit=quantization_bit,
        quantization_scheme=quantization_scheme,
        per_layer_quantization=per_layer_quantization,
    )
    scale, zero_point = min_max_observer(of_weight)
    _check_min_max_observer(
        test_case,
        np_weight,
        scale.numpy(),
        zero_point.numpy(),
        quantization_bit,
        quantization_scheme,
        quantization_formula,
        per_layer_quantization,
    )


class TestMinMaxObserver(flow.unittest.TestCase):
    @globaltest
    def test_min_max_observer(test_case):
        arg_dict = OrderedDict()
        arg_dict["device_type"] = ["cpu", "cuda"]
        arg_dict["weight_shape"] = [(9, 48, 24, 10)]
        arg_dict["quantization_bit"] = [8, 2]
        arg_dict["quantization_scheme"] = ["symmetric", "affine"]
        arg_dict["quantization_formula"] = ["google"]
        arg_dict["per_layer_quantization"] = [True, False]
        for arg in GenArgList(arg_dict):
            for placement in all_placement():
                for sbp in all_sbp(placement, valid_split_axis=[1, 2]):
                    _run_test_min_max_observer(test_case, placement, sbp, *arg)


if __name__ == "__main__":
    unittest.main()
