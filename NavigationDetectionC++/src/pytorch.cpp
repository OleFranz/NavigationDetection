#include "pytorch.h"


cv::Mat PyTorch::TensorToMat(torch::Tensor Tensor, int Width, int Height, int Channels) {
    Tensor = Tensor.permute({ 0, 2, 3, 1 });
    Tensor = Tensor.squeeze(0).detach();
    Tensor = Tensor.mul(255).clamp(0, 255).to(torch::kU8);
    Tensor = Tensor.to(torch::kCPU);
    cv::Mat Image(Height, Width, CV_8UC(Channels));
    std::memcpy((void*)Image.data, Tensor.data_ptr(), sizeof(torch::kU8)*Tensor.numel());
    return Image;
}


torch::Tensor PyTorch::MatToTensor(cv::Mat Frame) {
    cv::Mat FloatFrame;
    Frame.convertTo(FloatFrame, CV_32FC3, 1.0 / 255.0);
    torch::Tensor Tensor = torch::from_blob(FloatFrame.data, {1, FloatFrame.rows, FloatFrame.cols, Frame.channels()}, torch::kFloat32);
    Tensor = Tensor.permute({0, 3, 1, 2});
    return Tensor.clone();
}


torch::jit::Module PyTorch::Load(std::string Path) {
    std::cout << "Loading the model...\n > " << Path << std::endl;
    auto Model = torch::jit::Module();
    if (std::filesystem::exists(Path) == false) {
        std::cout << "Invalid path to the model!" << std::endl;
		return Model;
	}
    try {
        Model = torch::jit::load(Path, c10::kCPU);
        Model.eval();
        std::cout << "Successfully loaded the model!" << std::endl;
    } catch (torch::Error& e) {
        std::cout << "Failed to load the model!" << std::endl;
        std::cout << e.what() << std::endl;
        std::cout << "\nPossible reasons:\n > You built the app in debug mode with the LibTorch release version. Install the LibTorch debug version to use the model with debug app builds.\n > The model file is missing." << std::endl;
    } catch (std::exception& e) {
        std::cout << "Failed to load the model!" << std::endl;
        std::cout << e.what() << std::endl;
    }
    Variables::Model = Model;
    return Model;
}


torch::Tensor PyTorch::Detect(torch::Tensor Input, torch::jit::script::Module Model) {
    auto Output = Model.forward({Input}).toTensor();
    return Output;
}