#ifndef SDKCONTROLLER_H
#define SDKCONTROLLER_H

#include <windows.h>
#include <cstdint>
#include <cstring>

namespace SDKController {
    struct Controls {
        float Steering;
        float Acceleration;
        float Brake;
        float Clutch;
        bool Pause;
        bool ParkingBrake;
        bool Wipers;
        bool CruiseControl;
        bool CruiseControlIncrease;
        bool CruiseControlDecrease;
        bool CruiseControlReset;
        bool Lights;
        bool HighBeamLights;
        bool LeftIndicator;
        bool RightIndicator;
        bool LeftIndicatorHold;
        bool RightIndicatorHold;
        bool QuickPark;
        bool Drive;
        bool Reverse;
        bool CycleZoom;
        bool TripReset;
        bool WipersBack;
        bool WipersLevel0;
        bool WipersLevel1;
        bool WipersLevel2;
        bool WipersLevel3;
        bool WipersLevel4;
        bool Horn;
        bool AirHorn;
        bool LightHorn;
        bool Camera1;
        bool Camera2;
        bool Camera3;
        bool Camera4;
        bool Camera5;
        bool Camera6;
        bool Camera7;
        bool Camera8;
        bool RouteAdvisorZoomIn;
        bool RouteAdvisorZoomOut;
        bool AdaptiveCruiseControlMode;
        bool ShowHUDMirrors;
        bool HazardLights;
        bool Activate;
        bool AssistAct1;
        bool AssistAct2;
        bool AssistAct3;
        bool AssistAct4;
        bool AssistAct5;
    };

    extern HANDLE g_hMapFile;
    extern Controls* g_controls;

    bool Initialize();
    void Cleanup();
    void Reset();
    
    void SetSteering(float Value);
    void SetAcceleration(float Value);
    void SetBrake(float Value);
    void SetClutch(float Value);
    void SetPause(bool Value);
    void SetParkingBrake(bool Value);
    void SetWipers(bool Value);
    void SetCruiseControl(bool Value);
    void SetCruiseControlIncrease(bool Value);
    void SetCruiseControlDecrease(bool Value);
    void SetCruiseControlReset(bool Value);
    void SetLights(bool Value);
    void SetHighBeamLights(bool Value);
    void SetLeftIndicator(bool Value);
    void SetRightIndicator(bool Value);
    void SetLeftIndicatorHold(bool Value);
    void SetRightIndicatorHold(bool Value);
    void SetQuickPark(bool Value);
    void SetDrive(bool Value);
    void SetReverse(bool Value);
    void SetCycleZoom(bool Value);
    void SetTripReset(bool Value);
    void SetWipersBack(bool Value);
    void SetWipersLevel0(bool Value);
    void SetWipersLevel1(bool Value);
    void SetWipersLevel2(bool Value);
    void SetWipersLevel3(bool Value);
    void SetWipersLevel4(bool Value);
    void SetHorn(bool Value);
    void SetAirHorn(bool Value);
    void SetLightHorn(bool Value);
    void SetCamera1(bool Value);
    void SetCamera2(bool Value);
    void SetCamera3(bool Value);
    void SetCamera4(bool Value);
    void SetCamera5(bool Value);
    void SetCamera6(bool Value);
    void SetCamera7(bool Value);
    void SetCamera8(bool Value);
    void SetRouteAdvisorZoomIn(bool Value);
    void SetRouteAdvisorZoomOut(bool Value);
    void SetAdaptiveCruiseControlMode(bool Value);
    void SetShowHUDMirrors(bool Value);
    void SetHazardLights(bool Value);
    void SetActivate(bool Value);
    void SetAssistAct1(bool Value);
    void SetAssistAct2(bool Value);
    void SetAssistAct3(bool Value);
    void SetAssistAct4(bool Value);
    void SetAssistAct5(bool Value);
}

#endif