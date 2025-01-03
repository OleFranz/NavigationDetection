#ifndef VARIABLES_H
#define VARIABLES_H

#include <opencv2/opencv.hpp>
#include <torch/script.h>
#include <torch/torch.h>
#include <filesystem>
#include <algorithm>
#include <iostream>

#include "opencv.h"

namespace Variables {
    extern std::string PATH;
    extern std::string BUILD_TYPE;
    extern std::string BOLD;
    extern std::string ITALIC;
    extern std::string UNDERLINE;
    extern std::string RED;
    extern std::string GRAY;
    extern std::string BLUE;
    extern std::string CYAN;
    extern std::string GREEN;
    extern std::string NORMAL;
    extern std::string YELLOW;
    extern std::string PURPLE;

    extern torch::jit::Module Model;
};

#endif