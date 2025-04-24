import numpy as np
import win32gui
import time
import cv2
import mss


Model = None
SCT = mss.mss()
if len(SCT.monitors) < 2:
    Monitor = SCT.monitors[0]
else:
    Monitor = SCT.monitors[1]
ScreenX = Monitor["left"]
ScreenY = Monitor["top"]
ScreenWidth = Monitor["width"]
ScreenHeight = Monitor["height"]
LastWindowPositions = {}
LastForegroundWindows = {}
LastTrackWindowUpdates = {}
LastTrackWindowRouteAdvisorUpdates = {}


# MARK: Initialize()
def Initialize(Screen=None, Area=(None, None, None, None)):
    """
    Initialize the ScreenCapture module. Needs to be called before the use of Capture().

    Parameters
    ----------
    Screen : int
        The index of the screen to capture. Defaults to primary screen. Format: 0 = primary screen
    Area : tuple
        The area of the screen to capture in X1, Y1, X2, Y2. Defaults to entire screen.

    Returns
    -------
    None
    """
    global Display
    global Monitor
    global MonitorX1
    global MonitorY1
    global MonitorX2
    global MonitorY2
    global Cam
    global CaptureLibrary
    global RouteAdvisorSide
    global RouteAdvisorZoomCorrect
    global RouteAdvisorTabCorrect

    Display = Screen if Screen != None else 0
    Monitor = SCT.monitors[(Display + 1)]
    MonitorX1 = Area[0] if Area[0] != None else Monitor["left"]
    MonitorY1 = Area[1] if Area[1] != None else Monitor["top"]
    MonitorX2 = Area[2] if Area[2] != None else Monitor["width"]
    MonitorY2 = Area[3] if Area[3] != None else Monitor["height"]
    Cam = None
    CaptureLibrary = None
    RouteAdvisorSide = "Right"
    RouteAdvisorZoomCorrect = True
    RouteAdvisorTabCorrect = True

    try:

        try:

            from windows_capture import WindowsCapture, Frame, InternalCaptureControl
            Capture = WindowsCapture(
                cursor_capture=False,
                draw_border=False,
                monitor_index=Display + 1,
                window_name=None,
            )
            global WindowsCaptureFrame
            global StopWindowsCapture
            StopWindowsCapture = False
            @Capture.event
            def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
                global WindowsCaptureFrame
                global StopWindowsCapture
                WindowsCaptureFrame = frame.convert_to_bgr().frame_buffer.copy()
                if StopWindowsCapture:
                    StopWindowsCapture = False
                    capture_control.stop()
            @Capture.event
            def on_closed():
                print("Capture Session Closed")
            try:
                Control.stop()
            except:
                pass
            Control = Capture.start_free_threaded()

            CaptureLibrary = "WindowsCapture"

        except:

            import bettercam
            try:
                Cam.stop()
            except:
                pass
            try:
                Cam.close()
            except:
                pass
            try:
                Cam.release()
            except:
                pass
            try:
                del Cam
            except:
                pass
            Cam = bettercam.create(output_idx=Display, output_color="BGR")
            Cam.start()
            Cam.get_latest_frame()
            CaptureLibrary = "BetterCam"

    except:

        CaptureLibrary = "MSS"


# MARK: Capture()
def Capture(ImageType:str = "both"):
    """
    Get the latest frame from the screen. Automatically chooses the capture library. Can't be used in a thread!

    Parameters
    ----------
    ImageType : str
        The type of image to return. "both", "cropped", "full". Defaults to "both". "full" returns the entire screen, "cropped" returns the area of (X1, Y1, X2, Y2).

    Returns
    -------
    numpy.ndarray or numpy.ndarray, numpy.ndarray
        The return is based on the ImageType.
    """

    if CaptureLibrary.lower() == "windowscapture":

        try:

            img = cv2.cvtColor(np.array(WindowsCaptureFrame), cv2.COLOR_BGRA2BGR)
            if ImageType.lower() == "both":
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg, img
            elif ImageType.lower() == "cropped":
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg
            elif ImageType.lower() == "full":
                return img
            else:
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg, img

        except:

            return None if ImageType.lower() == "cropped" or ImageType.lower() == "full" else (None, None)

    elif CaptureLibrary.lower() == "bettercam":

        try:

            if Cam == None:
                Initialize()
            img = np.array(Cam.get_latest_frame())
            if ImageType.lower() == "both":
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg, img
            elif ImageType.lower() == "cropped":
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg
            elif ImageType.lower() == "full":
                return img
            else:
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg, img

        except:

            return None if ImageType.lower() == "cropped" or ImageType.lower() == "full" else (None, None)

    elif CaptureLibrary.lower() == "mss":

        try:

            fullMonitor = SCT.monitors[(Display + 1)]
            img = np.array(SCT.grab(fullMonitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            if ImageType.lower() == "both":
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg, img
            elif ImageType.lower() == "cropped":
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg
            elif ImageType.lower() == "full":
                return img
            else:
                croppedImg = img[MonitorY1:MonitorY2, MonitorX1:MonitorX2]
                return croppedImg, img

        except:

            return None if ImageType.lower() == "cropped" or ImageType.lower() == "full" else (None, None)


# MARK: GetScreenDimensions()
def GetScreenDimensions(Display=1):
    """
    Get the dimensions of the screen.

    Parameters
    ----------
    Display : int
        The index of the screen to get the dimensions of. Defaults to primary screen. Format: 1 = primary screen

    Returns
    -------
    int, int, int, int
        The dimensions of the screen. Format: (X, Y, Width, Height)
    """
    global ScreenX, ScreenY, ScreenWidth, ScreenHeight
    Monitor = SCT.monitors[Display]
    ScreenX = Monitor["left"]
    ScreenY = Monitor["top"]
    ScreenWidth = Monitor["width"]
    ScreenHeight = Monitor["height"]
    return ScreenX, ScreenY, ScreenWidth, ScreenHeight


def GetScreenIndex(X, Y):
    """
    Get the index of the screen that is closest to the given coordinates.

    Parameters
    ----------
    X : int
        The X coordinate.
    Y : int
        The Y coordinate.

    Returns
    -------
    int
        The index of the screen that is closest to the given coordinates. Format: 1 = primary screen
    """
    Monitors = SCT.monitors
    ClosestScreenIndex = None
    ClosestDistance = float('inf')
    for i, Monitor in enumerate(Monitors[1:]):
        CenterX = (Monitor['left'] + Monitor['left'] + Monitor['width']) // 2
        CenterY = (Monitor['top'] + Monitor['top'] + Monitor['height']) // 2
        Distance = ((CenterX - X) ** 2 + (CenterY - Y) ** 2) ** 0.5
        if Distance < ClosestDistance:
            ClosestScreenIndex = i + 1
            ClosestDistance = Distance
    return ClosestScreenIndex


# MARK: ValidateCaptureArea()
def ValidateCaptureArea(Display, X1, Y1, X2, Y2):
    """
    Validate the capture area, ensuring that it is within the bounds of the screen.

    Parameters
    ----------
    Display : int
        The index of the screen to validate the capture area for. Format: 1 = primary screen
    X1 : int
        The X coordinate of the top-left corner of the capture area.
    Y1 : int
        The Y coordinate of the top-left corner of the capture area.
    X2 : int
        The X coordinate of the bottom-right corner of the capture area.
    Y2 : int
        The Y coordinate of the bottom-right corner of the capture area.

    Returns
    -------
    int, int, int, int
        The validated capture area. Format: (X1, Y1, X2, Y2)
    """
    Monitor = SCT.monitors[Display]
    Width, Height = Monitor["width"], Monitor["height"]
    X1 = max(0, min(Width - 1, X1))
    X2 = max(0, min(Width - 1, X2))
    Y1 = max(0, min(Height - 1, Y1))
    Y2 = max(0, min(Height - 1, Y2))
    if X1 == X2:
        if X1 == 0:
            X2 = Width - 1
        else:
            X1 = 0
    if Y1 == Y2:
        if Y1 == 0:
            Y2 = Height - 1
        else:
            Y1 = 0
    return X1, Y1, X2, Y2


# MARK: IsForegroundWindow()
def IsForegroundWindow(Name="", Blacklist=[""]):
    """
    Check if the given window is in the foreground/is focused. The window name must contain 'Name' and all items in 'Blacklist' must not be in the window name.

    Parameters
    ----------
    Name : str
        The text which must be in the window name.
    Blacklist : list
        A list of strings that must not be in the window name.

    Returns
    -------
    bool
        True if the window is in the foreground/is focused, False otherwise.
    """
    Key = f"{Name}{Blacklist}"
    if Key not in LastForegroundWindows:
        LastForegroundWindows[Key] = [0, ScreenX, ScreenY, ScreenX + ScreenWidth, ScreenY + ScreenHeight]
    if LastForegroundWindows[Key][0] + 1 < time.time():
        HWND = None
        TopWindows = []
        IsForeground = LastForegroundWindows[Key][1]
        win32gui.EnumWindows(lambda HWND, TopWindows: TopWindows.append((HWND, win32gui.GetWindowText(HWND))), TopWindows)
        for HWND, WindowText in TopWindows:
            if Name in WindowText and all(BlacklistItem not in WindowText for BlacklistItem in Blacklist):
                IsForeground = (HWND == win32gui.GetForegroundWindow())
                break
        LastForegroundWindows[Key] = time.time(), IsForeground
        return IsForeground
    else:
        return LastForegroundWindows[Key][1]


# MARK: GetWindowPosition()
def GetWindowPosition(Name="", Blacklist=[""]):
    """
    Get the position of the given window. The window name must contain 'Name' and all items in 'Blacklist' must not be in the window name.

    Parameters
    ----------
    Name : str
        The text which must be in the window name.
    Blacklist : list
        A list of strings that must not be in the window name.

    Returns
    -------
    int, int, int, int
        The position of the window. Format: (X, Y, Width, Height)
    """
    global LastWindowPositions
    Key = f"{Name}{Blacklist}"
    if Key not in LastWindowPositions:
        LastWindowPositions[Key] = [0, ScreenX, ScreenY, ScreenX + ScreenWidth, ScreenY + ScreenHeight]
    if LastWindowPositions[Key][0] + 1 < time.time():
        HWND = None
        TopWindows = []
        Window = LastWindowPositions[Key][1], LastWindowPositions[Key][2], LastWindowPositions[Key][3], LastWindowPositions[Key][4]
        win32gui.EnumWindows(lambda HWND, TopWindows: TopWindows.append((HWND, win32gui.GetWindowText(HWND))), TopWindows)
        for HWND, WindowText in TopWindows:
            if Name in WindowText and all(BlacklistItem not in WindowText for BlacklistItem in Blacklist):
                RECT = win32gui.GetClientRect(HWND)
                TopLeft = win32gui.ClientToScreen(HWND, (RECT[0], RECT[1]))
                BottomRight = win32gui.ClientToScreen(HWND, (RECT[2], RECT[3]))
                Window = (TopLeft[0], TopLeft[1], BottomRight[0] - TopLeft[0], BottomRight[1] - TopLeft[1])
                break
        LastWindowPositions[Key] = time.time(), Window[0], Window[1], Window[0] + Window[2], Window[1] + Window[3]
        return Window[0], Window[1], Window[0] + Window[2], Window[1] + Window[3]
    else:
        return LastWindowPositions[Key][1], LastWindowPositions[Key][2], LastWindowPositions[Key][3], LastWindowPositions[Key][4]



# MARK: GetRouteAdvisorPosition()
def GetRouteAdvisorPosition(Name="", Blacklist=[""], Side="Right"):
    """
    Get the position of the Route Advisor window. The window name must contain 'Name' and all items in 'Blacklist' must not be in the window name.

    Parameters
    ----------
    Name : str
        The text which must be in the window name.
    Blacklist : list
        A list of strings that must not be in the window name.
    Side : str
        The side of the route advisor. Can be "Left" or "Right".

    Returns
    -------
    tuple : ((int, int), (int, int), (int, int), (int, int))\n
        `[0]`: (X, Y) Map Top Left\n
        `[1]`: (X, Y) Map Bottom Right\n
        `[2]`: (X, Y) Arrow Top Left\n
        `[3]`: (X, Y) Arrow Bottom Right\n
    """
    X1, Y1, X2, Y2 = GetWindowPosition(Name=Name, Blacklist=Blacklist)
    DistanceFromRight = 21
    DistanceFromBottom = 100
    Width = 420
    Height = 219
    Scale = (Y2 - Y1) / 1080

    if Side == "Left":
        X = X1 + (DistanceFromRight * Scale) - 1
        Y = Y1 + (Y2 - Y1) - (DistanceFromBottom * Scale + Height * Scale)
        LeftMapTopLeft = (round(X), round(Y))
        X = X1 + (DistanceFromRight * Scale + Width * Scale) - 1
        Y = Y1 + (Y2 - Y1) - (DistanceFromBottom * Scale)
        LeftMapBottomRight = (round(X), round(Y))
        X = LeftMapBottomRight[0] - (LeftMapBottomRight[0] - LeftMapTopLeft[0]) * 0.57 - 1
        Y = LeftMapBottomRight[1] - (LeftMapBottomRight[1] - LeftMapTopLeft[1]) * 0.575
        LeftArrowTopLeft = (round(X), round(Y))
        X = LeftMapBottomRight[0] - (LeftMapBottomRight[0] - LeftMapTopLeft[0]) * 0.43 - 1
        Y = LeftMapBottomRight[1] - (LeftMapBottomRight[1] - LeftMapTopLeft[1]) * 0.39
        LeftArrowBottomRight = (round(X), round(Y))
        return LeftMapTopLeft, LeftMapBottomRight, LeftArrowTopLeft, LeftArrowBottomRight

    if Side == "Right":
        X = X1 + (X2 - X1) - (DistanceFromRight * Scale + Width * Scale)
        Y = Y1 + (Y2 - Y1) - (DistanceFromBottom * Scale + Height * Scale)
        RightMapTopLeft = (round(X), round(Y))
        X = X1 + (X2 - X1) - (DistanceFromRight * Scale)
        Y = Y1 + (Y2 - Y1) - (DistanceFromBottom * Scale)
        RightMapBottomRight = (round(X), round(Y))
        X = RightMapBottomRight[0] - (RightMapBottomRight[0] - RightMapTopLeft[0]) * 0.57
        Y = RightMapBottomRight[1] - (RightMapBottomRight[1] - RightMapTopLeft[1]) * 0.575
        RightArrowTopLeft = (round(X), round(Y))
        X = RightMapBottomRight[0] - (RightMapBottomRight[0] - RightMapTopLeft[0]) * 0.43
        Y = RightMapBottomRight[1] - (RightMapBottomRight[1] - RightMapTopLeft[1]) * 0.39
        RightArrowBottomRight = (round(X), round(Y))
        return RightMapTopLeft, RightMapBottomRight, RightArrowTopLeft, RightArrowBottomRight


# MARK: TrackWindow()
def TrackWindow(Name="", Blacklist=[""], Rate=2):
    """
    Automatically update the Screen and Area which were set with Initialize(). The window name must contain 'Name' and all items in 'Blacklist' must not be in the window name.

    Parameters
    ----------
    Name : str
        The text which must be in the window name.
    Blacklist : list
        A list of strings that must not be in the window name.
    Rate : int
        The update rate in Hz, defaults to 2.

    Returns
    -------
    None
    """
    Key = f"{Name}{Blacklist}"
    if Key not in LastTrackWindowUpdates:
        LastTrackWindowUpdates[Key] = 0
    if Rate > 0:
        if LastTrackWindowUpdates[Key] + 1/Rate > time.time():
            return
    global StopWindowsCapture, MonitorX1, MonitorY1, MonitorX2, MonitorY2
    X1, Y1, X2, Y2 = GetWindowPosition(Name=Name, Blacklist=Blacklist)
    ScreenX, ScreenY, _, _ = GetScreenDimensions(GetScreenIndex((X1 + X2) / 2, (Y1 + Y2) / 2))
    if MonitorX1 != X1 - ScreenX or MonitorY1 != Y1 - ScreenY or MonitorX2 != X2 - ScreenX or MonitorY2 != Y2 - ScreenY:
        ScreenIndex = GetScreenIndex((X1 + X2) / 2, (Y1 + Y2) / 2)
        if Display != ScreenIndex - 1:
            if CaptureLibrary == "WindowsCapture":
                StopWindowsCapture = True
                while StopWindowsCapture == True:
                    time.sleep(0.01)
            Initialize(Screen=ScreenIndex - 1)
        MonitorX1, MonitorY1, MonitorX2, MonitorY2 = ValidateCaptureArea(ScreenIndex, X1 - ScreenX, Y1 - ScreenY, X2 - ScreenX, Y2 - ScreenY)
    LastTrackWindowUpdates[Key] = time.time()


# MARK: TrackWindowRouteAdvisor()
def TrackWindowRouteAdvisor(Name="", Blacklist=[""], Side="Right", Rate=2):
    """
    Automatically update the Screen and Area which were set with Initialize(). The window name must contain 'Name' and all items in 'Blacklist' must not be in the window name.

    Parameters
    ----------
    Name : str
        The text which must be in the window name.
    Blacklist : list
        A list of strings that must not be in the window name.
    Side : str
        The side of the route advisor. Can be "Left" or "Right".
    Rate : int
        The update rate in Hz, defaults to 2.

    Returns
    -------
    None
    """
    Key = f"{Name}{Blacklist}{Side}"
    if Key not in LastTrackWindowRouteAdvisorUpdates:
        LastTrackWindowRouteAdvisorUpdates[Key] = 0
    if Rate > 0:
        if LastTrackWindowRouteAdvisorUpdates[Key] + 1/Rate > time.time():
            return
    global StopWindowsCapture, MonitorX1, MonitorY1, MonitorX2, MonitorY2
    MapTopLeft, MapBottomRight, ArrowTopLeft, ArrowBottomRight = GetRouteAdvisorPosition(Name=Name, Blacklist=Blacklist, Side=Side)
    ScreenX, ScreenY, _, _ = GetScreenDimensions(GetScreenIndex((MapTopLeft[0] + MapBottomRight[0]) / 2, (MapTopLeft[1] + MapBottomRight[1]) / 2))
    if MonitorX1 != MapTopLeft[0] - ScreenX or MonitorY1 != MapTopLeft[1] - ScreenY or MonitorX2 != MapBottomRight[0] - ScreenX or MonitorY2 != MapBottomRight[1] - ScreenY:
        ScreenIndex = GetScreenIndex((MapTopLeft[0] + MapBottomRight[0]) / 2, (MapTopLeft[1] + MapBottomRight[1]) / 2)
        if Display != ScreenIndex - 1:
            if CaptureLibrary == "WindowsCapture":
                StopWindowsCapture = True
                while StopWindowsCapture == True:
                    time.sleep(0.01)
            Initialize(Screen=ScreenIndex - 1)
        MonitorX1, MonitorY1, MonitorX2, MonitorY2 = ValidateCaptureArea(ScreenIndex, MapTopLeft[0] - ScreenX, MapTopLeft[1] - ScreenY, MapBottomRight[0] - ScreenX, MapBottomRight[1] - ScreenY)
    LastTrackWindowRouteAdvisorUpdates[Key] = time.time()