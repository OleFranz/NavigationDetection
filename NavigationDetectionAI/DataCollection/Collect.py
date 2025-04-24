from TruckSimAPI import scsTelemetry as SCSTelemetry
import ScreenCapture
import SimpleWindow
import keyboard
import json
import time
import cv2
import os



# Settings
FPS = 1
enable_key = "f"
window_size = (420, 219)
window_position = (4, 857)
path = os.path.join(os.path.dirname(__file__), "Raw")
# --------



api = SCSTelemetry()
ScreenCapture.Initialize()
window = SimpleWindow.Window(name="NavigationDetectionAI Data Collection",
                             size=window_size,
                             position=window_position,
                             title_bar_color=(0, 0, 127),
                             border_color=(0, 0, 127),
                             resizable=False,
                             topmost=True,
                             foreground=True,
                             minimized=False,
                             undestroyable=True,
                             icon="",
                             no_warnings=False)

os.makedirs(path, exist_ok=True)

enabled = False
last_enable_key_pressed = False
last_capture_time = time.perf_counter()


while True:
    start = time.perf_counter()

    enable_key_pressed = keyboard.is_pressed(enable_key)

    if enable_key_pressed and not last_enable_key_pressed:
        enabled = not enabled
        window.set_title_bar_color((0, 127, 0) if enabled else (0, 0, 127))
        window.set_border_color((0, 127, 0) if enabled else (0, 0, 127))

    last_enable_key_pressed = enable_key_pressed


    is_foreground = ScreenCapture.IsForegroundWindow(Name="Truck Simulator", Blacklist=["Discord"])

    ScreenCapture.TrackWindowRouteAdvisor(Name="Truck Simulator", Blacklist=["Discord"], Side="Right", Rate=2)
    frame = ScreenCapture.Capture(ImageType="cropped")
    if type(frame) == type(None): continue

    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    if frame_width <= 0 or frame_height <= 0: continue


    if enabled and is_foreground and time.perf_counter() - last_capture_time > 1/FPS:
        last_capture_time = time.perf_counter()

        APIDATA = api.update()

        name = str(time.time()).replace(".", "_")

        try:
            if APIDATA["sdkActive"] == False: continue
            if APIDATA["pause"] == True: continue
            if APIDATA["scsValues"]["game"] == "unknown": continue

            with open(os.path.join(path, f"{name}.json"), "w") as f:
                json.dump(APIDATA, f, indent=4)
            cv2.imwrite(os.path.join(path, f"{name}.png"), frame, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        except:
            try: os.remove(os.path.join(path, f"{name}.json"))
            except: pass
            try: os.remove(os.path.join(path, f"{name}.png"))
            except: pass


    window.show(frame)

    time_to_sleep = 1/30 - (time.perf_counter() - start)
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)