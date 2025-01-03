#include "variables.h"

// This needs to be here for some reason
#define WIN32_LEAN_AND_MEAN
#define VC_EXTRALEAN
#include <Windows.h>

namespace Variables {
    std::string GetExePath() {
        std::string PATH = "";
        wchar_t wc[260] = {0};
        GetModuleFileNameW(NULL, wc, 260);
        std::wstring ws(wc);
        transform(ws.begin(), ws.end(), back_inserter(PATH), [](wchar_t c) { return (char)c; });
        return PATH.substr(0, PATH.rfind("\\") + 1);
    }

    std::string PATH = GetExePath();


    #ifdef BUILD_TYPE_RELEASE
        std::string BUILD_TYPE = "Release";
    #elif defined(BUILD_TYPE_DEBUG)
        std::string BUILD_TYPE = "Debug";
    #endif


    std::string BOLD = "\033[1m";
    std::string ITALIC = "\033[3m";
    std::string UNDERLINE = "\033[4m";

    std::string RED = "\033[91m";
    std::string GRAY = "\033[90m";
    std::string BLUE = "\033[94m";
    std::string CYAN = "\033[96m";
    std::string GREEN = "\033[92m";
    std::string NORMAL = "\033[0m";
    std::string YELLOW = "\033[93m";
    std::string PURPLE = "\033[95m";

    torch::jit::Module Model = torch::jit::Module();
}