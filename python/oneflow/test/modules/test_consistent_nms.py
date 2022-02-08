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

import oneflow as flow
import oneflow.unittest


from oneflow.test_utils.automated_test_util import *
from test_nms import create_tensors_with_iou
from test_nms import nms_np


def _test_nms(test_case, placement, sbp):
    iou = 0.5
    boxes, scores = create_tensors_with_iou(800, iou)
    boxes = flow.tensor(boxing, dtype=flow.float32).to_consistent(placement, sbp)
    scores = flow.tensor(scores, dtype=flow.float32).to_consistent(placement, sbp)
    keep_np = nms_np(boxes.numpy(), scores.numpy(), iou)
    keep = flow.nms(boxes, scores, iou)
    test_case.assertTrue(np.allclose(keep.numpy(), keep_np))


class TestNMS(flow.unittest.TestCase):
    @consistent
    def test_nms(test_case):
        for placement in all_placement():
            for sbp in all_sbp(placement, max_dim=1):
                _test_nms(test_case, placement, sbp)


if __name__ == "__main__":
    unittest.main()