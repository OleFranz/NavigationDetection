#include "NavigationDetection.h"

int main() {
	SDKController::Initialize();
	torch::jit::Module Model = PyTorch::Load(Variables::PATH + "Model.pt");

	cv::Mat Frame;
	cv::Mat Screenshot;
	float Steering = 0.0f;
	while (true) {

		auto [MapTopLeft, MapBottomRight, ArrowTopLeft, ArrowBottomRight] = ScreenCapture::GetRouteAdvisorPosition("Automatic");
		Screenshot = ScreenCapture::TakeScreenshot(std::get<0>(MapTopLeft), std::get<1>(MapTopLeft), std::get<0>(MapBottomRight), std::get<1>(MapBottomRight));
		cv::imshow("Screenshot", Screenshot);
		cv::waitKey(1);

		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}

	if (Variables::BUILD_TYPE == "Release") {
		system("pause");
	}
}