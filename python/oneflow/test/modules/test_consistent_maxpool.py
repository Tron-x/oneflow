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
import torch as pytorch
import oneflow.unittest

from collections import OrderedDict
from oneflow.test_utils.automated_test_util import *
from test_maxpool import unpack_indices
from test_util import GenArgList
from oneflow.nn.common_types import _size_1_t, _size_2_t, _size_3_t
from oneflow.test_utils.automated_test_util.util import broadcast


@autotest(n=1, auto_backward=False, check_graph=False)
def _test_maxpool1d_functional(test_case, placement, sbp):
    return_indices = random().to(bool).value()
    dim0 = random().to(int).value() * 8
    dim1 = random().to(int).value() * 8
    x = random_tensor(ndim=3, dim0=dim0, dim1=dim1, dim2=random(20, 22)).to_consistent(
        placement, sbp
    )
    y = torch.nn.functional.max_pool1d(
        x,
        kernel_size=random(4, 6).to(int),
        stride=random(1, 3).to(int),
        padding=random(1, 3).to(int),
        dilation=random(2, 4).to(int),
        ceil_mode=random().to(bool),
        return_indices=return_indices,
    )
    if return_indices:
        return unpack_indices(y)
    else:
        return y, y.sum().backward()


@autotest(n=1, auto_backward=False, check_graph=False)
def _test_maxpool2d_functional(test_case, placement, sbp):
    return_indices = random().to(bool).value()
    dim0 = random().to(int).value() * 8
    dim1 = random().to(int).value() * 8
    device = random_device()
    x = random_tensor(
        ndim=4, dim0=dim0, dim1=dim1, dim2=random(20, 22), dim3=random(20, 22)
    ).to_consistent(placement, sbp)
    y = torch.nn.functional.max_pool2d(
        x,
        kernel_size=random(4, 6).to(int),
        stride=random(1, 3).to(int),
        padding=random(1, 3).to(int),
        dilation=random(2, 4).to(int),
        ceil_mode=random().to(bool),
        return_indices=return_indices,
    )

    if return_indices:
        return unpack_indices(y)
    else:
        return y, y.sum().backward()


@autotest(n=1, auto_backward=False, check_graph=False)
def _test_maxpool3d_functional(test_case, placement, sbp):
    return_indices = random().to(bool).value()
    dim0 = random().to(int).value() * 8
    dim1 = random().to(int).value() * 8
    device = random_device()
    x = random_tensor(
        ndim=5,
        dim0=dim0,
        dim1=dim1,
        dim2=random(20, 22),
        dim3=random(20, 22),
        dim4=random(20, 22),
    ).to_consistent(placement, sbp)
    y = torch.nn.functional.max_pool3d(
        x,
        kernel_size=random(4, 6).to(int),
        stride=random(1, 3).to(int),
        padding=random(1, 3).to(int),
        dilation=random(2, 4).to(int),
        ceil_mode=random().to(bool),
        return_indices=return_indices,
    )

    if return_indices:
        return unpack_indices(y)
    else:
        return y, y.sum().backward()


@autotest(n=1, auto_backward=False, check_graph=False)
def _test_maxpool1d(test_case, placement, sbp):
    return_indices = random().to(bool).value()
    dim0 = random().to(int).value() * 8
    dim1 = random().to(int).value() * 8
    m = torch.nn.MaxPool1d(
        kernel_size=random(4, 6).to(_size_1_t),
        stride=random(1, 3).to(_size_1_t),
        padding=random(1, 3).to(_size_1_t),
        dilation=random(2, 4).to(_size_1_t),
        ceil_mode=random(),
        return_indices=return_indices,
    )
    m.train(random())
    x = random_tensor(ndim=3, dim0=dim0, dim1=dim1, dim2=random(20, 22)).to_consistent(
        placement, sbp
    )
    y = m(x)
    if return_indices:
        return unpack_indices(y)
    else:
        return y, y.sum().backward()


@autotest(n=1, auto_backward=False, check_graph=False)
def _test_maxpool2d(test_case, placement, sbp):
    return_indices = random().to(bool).value()
    dim0 = random().to(int).value() * 8
    dim1 = random().to(int).value() * 8
    m = torch.nn.MaxPool2d(
        kernel_size=random(4, 6).to(_size_1_t),
        stride=random(1, 3).to(_size_1_t),
        padding=random(1, 3).to(_size_1_t),
        dilation=random(2, 4).to(_size_1_t),
        ceil_mode=random(),
        return_indices=return_indices,
    )
    m.train(random())
    x = random_tensor(
        ndim=4, dim0=dim0, dim1=dim1, dim2=random(20, 22), dim3=random(20, 22)
    ).to_consistent(placement, sbp)
    y = m(x)
    if return_indices:
        return unpack_indices(y)
    else:
        return y, y.sum().backward()


@autotest(n=1, auto_backward=False, check_graph=False)
def _test_maxpool3d(test_case, placement, sbp):
    return_indices = random().to(bool).value()
    dim0 = random().to(int).value() * 8
    dim1 = random().to(int).value() * 8
    m = torch.nn.MaxPool3d(
        kernel_size=random(4, 6).to(_size_3_t),
        stride=random(1, 3).to(_size_3_t),
        padding=random(1, 3).to(_size_3_t),
        dilation=random(2, 4).to(_size_3_t),
        ceil_mode=random(),
        return_indices=return_indices,
    )
    m.train(random())
    device = random_device()
    m.to(device)
    x = random_tensor(
        ndim=5,
        dim0=dim0,
        dim1=dim1,
        dim2=random(20, 22),
        dim3=random(20, 22),
        dim4=random(20, 22),
    ).to(device)
    y = m(x)

    if return_indices:
        return unpack_indices(y)
    else:
        return y, y.sum().backward()


def _test_maxpool2d_channel_last(
    test_case, shape, kernel_size, stride, padding, dilation, ceil_mode, placement
):
    os.environ["ONEFLOW_ENABLE_NHWC"] = "1"
    shape = broadcast(shape)
    kernel_size = broadcast(kernel_size)
    stride = broadcast(stride)
    padding = broadcast(padding)
    dilation = broadcast(dilation)
    ceil_mode = broadcast(ceil_mode)

    arr = np.random.randn(*shape)
    m1 = flow.nn.MaxPool2d(
        kernel_size=kernel_size,
        stride=stride,
        padding=padding,
        dilation=dilation,
        ceil_mode=ceil_mode,
    )

    x2 = pytorch.tensor(arr.transpose(0, 3, 1, 2), dtype=pytorch.float64)
    m2 = pytorch.nn.MaxPool2d(
        kernel_size=kernel_size,
        stride=stride,
        padding=padding,
        dilation=dilation,
        ceil_mode=ceil_mode,
    )
    y2 = m2(x2).permute(0, 2, 3, 1)

    for sbp in all_sbp(placement, max_dim=2):
        x1 = flow.tensor(arr, dtype=flow.float64).to_consistent(placement, sbp)
        y1 = m1(x1)
        test_case.assertTrue(
            np.allclose(
                y1.detach().cpu().numpy(), y2.detach().cpu().numpy(), 1e-4, 1e-4
            )
        )
    os.environ["ONEFLOW_ENABLE_NHWC"] = "0"


class TestMaxPool(flow.unittest.TestCase):
    @consistent
    def test_maxpool(test_case):
        for placement in all_placement():
            for sbp in all_sbp(placement, max_dim=1):
                _test_maxpool1d_functional(test_case, placement, sbp)
                _test_maxpool2d_functional(test_case, placement, sbp)
                _test_maxpool3d_functional(test_case, placement, sbp)
                _test_maxpool1d(test_case, placement, sbp)
                # TODO(): infer shape error
                # _test_maxpool2d(test_case, placement, sbp)
                _test_maxpool3d(test_case, placement, sbp)

    @unittest.skip("Maybe result shape is wrong.")
    @consistent
    def test_maxpool2d_channel_last(test_case):
        arg_dict = OrderedDict()
        arg_dict["test_fun"] = [_test_maxpool2d_channel_last]
        arg_dict["shape"] = [(16, 112, 27, 3), (56, 72, 14, 10), (128, 1792, 224, 3)]
        arg_dict["kernel_size"] = [3, (2, 3), (3, 4)]
        arg_dict["stride"] = [1, (1, 2), 2]
        arg_dict["padding"] = [0, (0, 1)]
        arg_dict["dilation"] = [1, (1, 2), 2]
        arg_dict["ceil_mode"] = [True, False]
        arg_dict["placement"] = list(all_placement())
        for arg in GenArgList(arg_dict):
            arg[0](test_case, *arg[1:])


if __name__ == "__main__":
    unittest.main()