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
#include "oneflow/core/comm_network/ibverbs/ibverbs_message_pool.h"
#include "oneflow/core/comm_network/ibverbs/ibverbs_qp.h"

#if defined(WITH_RDMA) && defined(OF_PLATFORM_POSIX)

namespace oneflow {

IBVerbsMessagePool::~IBVerbsMessagePool() {
  size_t mr_buf_size = ibv_mr_buf_.size();
  for (size_t i = 0; i < mr_buf_size; i++) {
    ibv_mr* mr = ibv_mr_buf_[i];
    CHECK_EQ(ibv::wrapper.ibv_dereg_mr(mr), 0);
  }
  size_t memory_buf_size = memory_buf_.size();
  for (size_t i = 0; i < memory_buf_size; i++) { free(memory_buf_[i]); }
  ibv_mr_buf_.clear();
  memory_buf_.clear();
}

IBVerbsMessagePool::IBVerbsMessagePool(ibv_pd* pd, uint32_t num_msg_per_bluk_allocation)
    : pd_(pd), num_msg_per_bluk_allocation_(num_msg_per_bluk_allocation) {}

void IBVerbsMessagePool::BulkAllocMessage() {
  size_t message_size = sizeof(ActorMsg);
  size_t register_memory_size = message_size * num_msg_per_bluk_allocation_;
  char* addr = (char*)malloc(register_memory_size);
  ibv_mr* mr = ibv::wrapper.ibv_reg_mr_wrap(
      pd_, addr, register_memory_size,
      IBV_ACCESS_LOCAL_WRITE | IBV_ACCESS_REMOTE_WRITE | IBV_ACCESS_REMOTE_READ);
  CHECK(mr);
  ibv_mr_buf_.push_back(mr);
  memory_buf_.push_back(addr);
  for (size_t i = 0; i < num_msg_per_bluk_allocation_; i++) {
    char* split_addr = addr + message_size * i;
    ActorMsgMR* msg_mr = new ActorMsgMR(mr, split_addr, message_size);
    message_buf_.push_back(msg_mr);
  }
}

ActorMsgMR* IBVerbsMessagePool::GetMessage() {
  std::unique_lock<std::mutex> msg_buf_lck(message_buf_mutex_);
  if (!message_buf_.empty()) {
    return GetMessageFromBuf();
  } else {
    BulkAllocMessage();
    return GetMessageFromBuf();
  }
}

ActorMsgMR* IBVerbsMessagePool::GetMessageFromBuf() {
  ActorMsgMR* msg_mr = message_buf_.back();
  message_buf_.pop_back();
  return msg_mr;
}

void IBVerbsMessagePool::PutMessage(ActorMsgMR* msg_mr) {
  std::unique_lock<std::mutex> msg_buf_lck(message_buf_mutex_);
  message_buf_.push_back(msg_mr);
}

}  // namespace oneflow

#endif  // WITH_RDMA && OF_PLATFORM_POSIX