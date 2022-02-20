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
#include "oneflow/core/ipc/shared_memory.h"
#include "oneflow/core/common/util.h"
#include "oneflow/core/common/pcheck.h"
#include "oneflow/core/common/str_util.h"
#include "oneflow/core/common/optional.h"
#ifdef __linux__
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <error.h>
#endif

namespace oneflow {
namespace ipc {

namespace {

#ifdef __linux__

// return errno
int ShmOpen(const std::string& shm_name, bool create, int* fd) {
  *fd = shm_open(shm_name.c_str(), (create ? O_CREAT : 0) | O_EXCL | O_RDWR, S_IRUSR | S_IWUSR);
  return *fd == -1 ? errno : 0;
}

// return errno
int ShmOpen(std::string* shm_name, int* fd) {
  int err = EEXIST;
  while (true) {
    static constexpr int kNameLength = 8;
    *shm_name = std::string("/ofshm_") + GenAlphaNumericString(kNameLength);
    err = ShmOpen(*shm_name, true, fd);
    if (err != EEXIST) { return err; }
  }
  return err;
}

int ShmMap(int fd, const size_t shm_size, void** ptr) {
  *ptr = mmap(NULL, shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  return (*ptr == MAP_FAILED) ? errno : 0;
}

#endif

}  // namespace

SharedMemory::~SharedMemory() {
  if (buf_ != nullptr) { CHECK_JUST(Close()); }
}

Maybe<SharedMemory> SharedMemory::Open(const Optional<std::string>& opt_shm_name, size_t shm_size) {
#ifdef __linux__
  int fd = 0;
  std::string shm_name;
  if (opt_shm_name.has_value()) {
    shm_name = *JUST(opt_shm_name);
    PCHECK_OR_RETURN(ShmOpen(shm_name, true, &fd));
    std::cout << "create " << shm_name << std::endl;
  } else {
    PCHECK_OR_RETURN(ShmOpen(&shm_name, &fd));
  }
  PCHECK_OR_RETURN(posix_fallocate(fd, 0, shm_size)) << ReturnEmptyStr([&] { close(fd); });
  void* ptr = nullptr;
  PCHECK_OR_RETURN(ShmMap(fd, shm_size, &ptr)) << ReturnEmptyStr([&] { close(fd); });
  close(fd);
  std::memset(ptr, 0, shm_size);
  return std::shared_ptr<SharedMemory>(new SharedMemory(static_cast<char*>(ptr), shm_name, shm_size));
#else
  TODO_THEN_RETURN();
#endif
}

Maybe<SharedMemory> SharedMemory::Open(const std::string& shm_name) {
#ifdef __linux__
  int fd = 0;
  PCHECK_OR_RETURN(ShmOpen(shm_name, false, &fd));
  struct stat st;  // NOLINT
  PCHECK_OR_RETURN(fstat(fd, &st)) << ReturnEmptyStr([&] { close(fd); });
  size_t shm_size = st.st_size;
  void* ptr = nullptr;
  PCHECK_OR_RETURN(ShmMap(fd, shm_size, &ptr)) << ReturnEmptyStr([&] { close(fd); });
  close(fd);
  return std::shared_ptr<SharedMemory>(new SharedMemory(static_cast<char*>(ptr), shm_name, shm_size));
#else
  TODO_THEN_RETURN();
#endif
}

Maybe<void> SharedMemory::Close() {
#ifdef __linux__
  PCHECK_OR_RETURN(munmap(buf_, size_));
  buf_ = nullptr;
  return Maybe<void>::Ok();
#else
  TODO_THEN_RETURN();
#endif
}

Maybe<void> SharedMemory::Unlink() {
#ifdef __linux__
  return UnlinkByName(name_);
#else
  TODO_THEN_RETURN();
#endif
}

Maybe<void> SharedMemory::UnlinkByName(const std::string& name) {
#ifdef __linux__
  PCHECK_OR_RETURN(shm_unlink(name.c_str()));
  return Maybe<void>::Ok();
#else
  TODO_THEN_RETURN();
#endif
}

}  // namespace ipc
}  // namespace oneflow
