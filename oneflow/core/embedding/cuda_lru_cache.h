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
#ifndef ONEFLOW_EMBEDDING_CUDA_LRU_CACHE_H_
#define ONEFLOW_EMBEDDING_CUDA_LRU_CACHE_H_

#include "oneflow/core/embedding/cache.h"
#include "oneflow/core/common/data_type.h"

namespace oneflow {

namespace embedding {

struct CudaLruCacheOptions {
  uint32_t log2_n_set;
  uint32_t line_size;
  uint32_t max_query_length;
  DataType key_type;
  DataType value_type;
};

std::unique_ptr<Cache> NewCudaLruCache(const CudaLruCacheOptions& options);

}  // namespace embedding

}  // namespace oneflow

#endif  // ONEFLOW_EMBEDDING_CUDA_LRU_CACHE_H_