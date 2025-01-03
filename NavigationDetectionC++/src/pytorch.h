#ifndef PYTORCH_H
#define PYTORCH_H

#include <opencv2/opencv.hpp>
#include <torch/script.h>
#include <torch/torch.h>
#include <unordered_map>
#include <exception>
#include <iostream>
#include <sstream>
#include <utility>
#include <chrono>
#include <string>
#include <thread>
#include <vector>
#include <cmath>
#include <map>
#include <any>

#include "variables.h"
#include "opencv.h"

class PyTorch {
public:
    static cv::Mat TensorToMat(torch::Tensor Tensor, int Width, int Height, int Channels);
    static torch::Tensor MatToTensor(cv::Mat Frame);

    static torch::jit::Module Load(std::string Path);
    static torch::Tensor Detect(torch::Tensor Input, torch::jit::Module Model);
};

#endif