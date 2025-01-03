#include "NavigationDetection.h"

int main() {
	SDKController::Initialize();
	torch::jit::Module Model = PyTorch::Load(Variables::PATH + "Model.pt");

	cv::Mat Frame;
	cv::Mat Screenshot;
	double LastScreenCaptureCheck = 0.0;
	double CurrentTime = 0.0;
	double StartTime = 0.0;
	double EndTime = 0.0;
	while (true) {
		CurrentTime = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch()).count() / 1000000000.0;
		StartTime = CurrentTime;

		Frame = ScreenCapture::GetLatestFrame();
		cv::imshow("Frame", Frame);
		cv::waitKey(1);

		//auto [MapTopLeft, MapBottomRight, ArrowTopLeft, ArrowBottomRight] = ScreenCapture::GetRouteAdvisorPosition("Automatic");
		//Screenshot = ScreenCapture::TakeScreenshot(std::get<0>(MapTopLeft), std::get<1>(MapTopLeft), std::get<0>(MapBottomRight), std::get<1>(MapBottomRight));
		//cv::imshow("Screenshot", Screenshot);
		//cv::waitKey(1);

		EndTime = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch()).count() / 1000000000.0;

		std::cout << "FPS: " << 1.0 / (EndTime - StartTime) << std::endl;
	}

	if (Variables::BUILD_TYPE == "Release") {
		system("pause");
	}
}