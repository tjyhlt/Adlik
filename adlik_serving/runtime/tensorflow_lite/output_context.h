// Copyright 2019 ZTE corporation. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

#ifndef ADLIK_SERVING_RUNTIME_TENSORFLOW_LITE_OUTPUT_CONTEXT_H
#define ADLIK_SERVING_RUNTIME_TENSORFLOW_LITE_OUTPUT_CONTEXT_H

#include "adlik_serving/framework/domain/dims_list.h"
#include "adlik_serving/runtime/tensorflow_lite/tensor_utilities.h"

namespace adlik {
namespace serving {
class OutputContext {
public:
  const int tensorIndex;

private:
  std::string name;

public:
  const tensorflow::DataType dataType;

private:
  tensor_tools::TfLiteTensorReader reader;

  // Cache.

  DimsList dimsListCache;

  OutputContext(int tensorIndex,
                std::string name,
                tensorflow::DataType dataType,
                tensor_tools::TfLiteTensorReader reader);

public:
  const std::string& getName() const;
  const DimsList& calculateDimsList(const TfLiteIntArray& dims) noexcept;

  template <class F>
  decltype(auto) useReader(F&& f) {
    return this->reader.visit(std::forward<F>(f));
  }

  static OutputContext fromTfLiteTensor(int tensorIndex, const TfLiteTensor& tfLiteTensor);
};
}  // namespace serving
}  // namespace adlik

#endif  // ADLIK_SERVING_RUNTIME_TENSORFLOW_LITE_OUTPUT_CONTEXT_H
