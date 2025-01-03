#include "sdkcontroller.h"

namespace SDKController {
    HANDLE g_hMapFile = NULL;
    Controls* g_controls = nullptr;

    bool Initialize() {
        g_hMapFile = CreateFileMappingW(
            INVALID_HANDLE_VALUE, 
            NULL,
            PAGE_READWRITE,
            0,
            sizeof(Controls),
            L"Local\\SCSControls"
        );

        if (!g_hMapFile) return false;

        g_controls = (Controls*)MapViewOfFile(
            g_hMapFile,
            FILE_MAP_ALL_ACCESS,
            0,
            0,
            sizeof(Controls)
        );

        if (!g_controls) {
            CloseHandle(g_hMapFile);
            return false;
        }

        Reset();
        return true;
    }

    void Reset() {
        if (g_controls) {
            ZeroMemory(g_controls, sizeof(Controls));
        }
    }

    void Cleanup() {
        if (g_controls) {
            UnmapViewOfFile(g_controls);
            g_controls = nullptr;
        }
        if (g_hMapFile) {
            CloseHandle(g_hMapFile);
            g_hMapFile = NULL;
        }
    }

    void SetSteering(float Value) { if (g_controls) g_controls->Steering = Value; }
    void SetAcceleration(float Value) { if (g_controls) g_controls->Acceleration = Value; }
    void SetBrake(float Value) { if (g_controls) g_controls->Brake = Value; }
    void SetClutch(float Value) { if (g_controls) g_controls->Clutch = Value; }
    void SetPause(bool Value) { if (g_controls) g_controls->Pause = Value; }
    void SetParkingBrake(bool Value) { if (g_controls) g_controls->ParkingBrake = Value; }
    void SetWipers(bool Value) { if (g_controls) g_controls->Wipers = Value; }
    void SetCruiseControl(bool Value) { if (g_controls) g_controls->CruiseControl = Value; }
    void SetCruiseControlIncrease(bool Value) { if (g_controls) g_controls->CruiseControlIncrease = Value; }
    void SetCruiseControlDecrease(bool Value) { if (g_controls) g_controls->CruiseControlDecrease = Value; }
    void SetCruiseControlReset(bool Value) { if (g_controls) g_controls->CruiseControlReset = Value; }
    void SetLights(bool Value) { if (g_controls) g_controls->Lights = Value; }
    void SetHighBeamLights(bool Value) { if (g_controls) g_controls->HighBeamLights = Value; }
    void SetLeftIndicator(bool Value) { if (g_controls) g_controls->LeftIndicator = Value; }
    void SetRightIndicator(bool Value) { if (g_controls) g_controls->RightIndicator = Value; }
    void SetLeftIndicatorHold(bool Value) { if (g_controls) g_controls->LeftIndicatorHold = Value; }
    void SetRightIndicatorHold(bool Value) { if (g_controls) g_controls->RightIndicatorHold = Value; }
    void SetQuickPark(bool Value) { if (g_controls) g_controls->QuickPark = Value; }
    void SetDrive(bool Value) { if (g_controls) g_controls->Drive = Value; }
    void SetReverse(bool Value) { if (g_controls) g_controls->Reverse = Value; }
    void SetCycleZoom(bool Value) { if (g_controls) g_controls->CycleZoom = Value; }
    void SetTripReset(bool Value) { if (g_controls) g_controls->TripReset = Value; }
    void SetWipersBack(bool Value) { if (g_controls) g_controls->WipersBack = Value; }
    void SetWipersLevel0(bool Value) { if (g_controls) g_controls->WipersLevel0 = Value; }
    void SetWipersLevel1(bool Value) { if (g_controls) g_controls->WipersLevel1 = Value; }
    void SetWipersLevel2(bool Value) { if (g_controls) g_controls->WipersLevel2 = Value; }
    void SetWipersLevel3(bool Value) { if (g_controls) g_controls->WipersLevel3 = Value; }
    void SetWipersLevel4(bool Value) { if (g_controls) g_controls->WipersLevel4 = Value; }
    void SetHorn(bool Value) { if (g_controls) g_controls->Horn = Value; }
    void SetAirHorn(bool Value) { if (g_controls) g_controls->AirHorn = Value; }
    void SetLightHorn(bool Value) { if (g_controls) g_controls->LightHorn = Value; }
    void SetCamera1(bool Value) { if (g_controls) g_controls->Camera1 = Value; }
    void SetCamera2(bool Value) { if (g_controls) g_controls->Camera2 = Value; }
    void SetCamera3(bool Value) { if (g_controls) g_controls->Camera3 = Value; }
    void SetCamera4(bool Value) { if (g_controls) g_controls->Camera4 = Value; }
    void SetCamera5(bool Value) { if (g_controls) g_controls->Camera5 = Value; }
    void SetCamera6(bool Value) { if (g_controls) g_controls->Camera6 = Value; }
    void SetCamera7(bool Value) { if (g_controls) g_controls->Camera7 = Value; }
    void SetCamera8(bool Value) { if (g_controls) g_controls->Camera8 = Value; }
    void SetRouteAdvisorZoomIn(bool Value) { if (g_controls) g_controls->RouteAdvisorZoomIn = Value; }
    void SetRouteAdvisorZoomOut(bool Value) { if (g_controls) g_controls->RouteAdvisorZoomOut = Value; }
    void SetAdaptiveCruiseControlMode(bool Value) { if (g_controls) g_controls->AdaptiveCruiseControlMode = Value; }
    void SetShowHUDMirrors(bool Value) { if (g_controls) g_controls->ShowHUDMirrors = Value; }
    void SetHazardLights(bool Value) { if (g_controls) g_controls->HazardLights = Value; }
    void SetActivate(bool Value) { if (g_controls) g_controls->Activate = Value; }
    void SetAssistAct1(bool Value) { if (g_controls) g_controls->AssistAct1 = Value; }
    void SetAssistAct2(bool Value) { if (g_controls) g_controls->AssistAct2 = Value; }
    void SetAssistAct3(bool Value) { if (g_controls) g_controls->AssistAct3 = Value; }
    void SetAssistAct4(bool Value) { if (g_controls) g_controls->AssistAct4 = Value; }
    void SetAssistAct5(bool Value) { if (g_controls) g_controls->AssistAct5 = Value; }
}