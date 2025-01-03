#ifndef SCREENCAPTURE_H
#define SCREENCAPTURE_H

#include <opencv2/opencv.hpp>
#include <torch/script.h>
#include <torch/torch.h>
#include <windows.h>
#include <iostream>
#include <dwmapi.h>

#include "pytorch.h"

#pragma comment(lib, "dwmapi.lib")

class ScreenCapture {
public:
    static cv::Mat GetLatestFrame();
    static void SetCaptureArea(int X1, int Y1, int X2, int Y2);
    static cv::Mat TakeScreenshot(int X1, int Y1, int X2, int Y2);
    static std::tuple<int, int, int, int> GetScreenDimensions(int Display);
    static int GetScreenIndex(int X, int Y);
    static std::tuple<int, int, int, int> ValidateCaptureArea(int Display, int X1, int Y1, int X2, int Y2);
    static bool IsForegroundWindow(std::string Name, std::vector<std::string> Blacklist);
    static std::tuple<int, int, int, int> GetWindowPosition(std::string Name, std::vector<std::string> Blacklist);
    static std::tuple<std::tuple<int, int>, std::tuple<int, int>, std::tuple<int, int>, std::tuple<int, int>> GetRouteAdvisorPosition(std::string Side);
};

#endif