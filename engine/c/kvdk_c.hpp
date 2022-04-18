/* SPDX-License-Identifier: BSD-3-Clause
 * Copyright(c) 2021 Intel Corporation
 */

#include <cassert>
#include <cstdlib>
#include <cstring>

#include "../alias.hpp"
#include "kvdk/configs.hpp"
#include "kvdk/engine.h"
#include "kvdk/engine.hpp"
#include "kvdk/iterator.hpp"
#include "kvdk/status.h"
#include "kvdk/write_batch.hpp"

using kvdk::StringView;

using kvdk::Configs;
using kvdk::Engine;
using kvdk::HashIterator;
using kvdk::Iterator;
using kvdk::ListIterator;
using kvdk::Snapshot;
using kvdk::SortedCollectionConfigs;
using kvdk::WriteBatch;
using kvdk::WriteOptions;

extern "C" {

struct KVDKConfigs {
  Configs rep;
};

struct KVDKEngine {
  std::unique_ptr<Engine> rep;
};

struct KVDKWriteBatch {
  WriteBatch rep;
};
struct KVDKIterator {
  Iterator* rep;
};

struct KVDKListIterator {
  std::unique_ptr<ListIterator> rep;
};

struct KVDKHashIterator {
  std::unique_ptr<HashIterator> rep;
};

struct KVDKSnapshot {
  Snapshot* rep;
};

struct KVDKWriteOptions {
  WriteOptions rep;
};

struct KVDKSortedCollectionConfigs {
  SortedCollectionConfigs rep;
};

static char* CopyStringToChar(const std::string& str) {
  char* result = static_cast<char*>(malloc(str.size()));
  memcpy(result, str.data(), str.size());
  return result;
}

}  // extern "C"