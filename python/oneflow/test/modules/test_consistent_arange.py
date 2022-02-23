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
from collections import OrderedDict

import oneflow as flow
import oneflow.unittest
from oneflow.test_utils.automated_test_util import *

from test_util import GenArgDict


def _test_consistent_arange(test_case, start, end, step, placement, sbp):
    x = flow.arange(start, end, step, placement=placement, sbp=sbp)

    test_case.assertEqual(x.sbp, sbp)
    test_case.assertEqual(x.placement, placement)


def _test_graph_arange(test_case, start, end, step, placement, sbp):
    class ConsistentRandGraph(flow.nn.Graph):
        def __init__(self,):
            super().__init__()

        def build(self):
            x = flow.arange(start, end, step, placement=placement, sbp=sbp)
            return x

    model = ConsistentRandGraph()
    x = model()

    test_case.assertEqual(x.sbp, sbp)
    test_case.assertEqual(x.placement, placement)


class TestRandConsistent(flow.unittest.TestCase):
    @globaltest
    def test_arange_consistent(test_case):
        start_list = [i for i in range(1, 5, 1)]
        end_list = [i for i in range(10, 50, 10)]
        step_list = [i for i in range(1, 5, 1)]
        for start in start_list:
            for end in end_list:
                for step in step_list:
                    for placement in all_placement():
                        for sbp in all_sbp(
                            placement, max_dim=1, except_partial_sum=True
                        ):
                            _test_consistent_arange(
                                test_case, start, end, step, placement, sbp
                            )

    @unittest.skipIf(os.getenv("ONEFLOW_TEST_CPU_ONLY"), "only test cpu cases")
    @flow.unittest.skip_unless_1n2d()
    def test_rand_graph(test_case):
        arg_dict = OrderedDict()
        arg_dict["start"] = [i for i in range(1, 5, 1)]
        arg_dict["end"] = [i for i in range(10, 50, 10)]
        arg_dict["step"] = [i for i in range(1, 5, 1)]
        arg_dict["placement"] = [
            # 1d
            flow.placement("cpu", ranks=[0, 1]),
            flow.placement("cuda", ranks=[0, 1]),
            # 2d
            flow.placement("cpu", ranks=[[0, 1],]),
            flow.placement("cuda", ranks=[[0, 1],]),
        ]
        for args in GenArgDict(arg_dict):
            start = args["start"]
            end = args["end"]
            step = args["step"]
            placement = args["placement"]
            for sbp in all_sbp(placement, max_dim=1, except_partial_sum=True):
                _test_graph_arange(test_case, start, end, step, placement, sbp)


if __name__ == "__main__":
    unittest.main()
