import shutil
import numpy
import json
import cv2
import os



# Settings
resolution = (420, 219)
src_path = os.path.join(os.path.dirname(__file__), "Raw")
dst_path = os.path.join(os.path.dirname(__file__), "Processed")
# --------



shutil.rmtree(dst_path, ignore_errors=True)

os.makedirs(src_path, exist_ok=True)
os.makedirs(dst_path, exist_ok=True)

for file in os.listdir(src_path):
    file = str(file)
    if file.endswith(".png"):
        frame = cv2.imread(os.path.join(src_path, file), cv2.IMREAD_UNCHANGED)

        if frame.shape[0] != resolution[1] or frame.shape[1] != resolution[0]:
            frame = cv2.resize(frame, resolution)

        lower_red = numpy.array([0, 0, 160])
        upper_red = numpy.array([110, 110, 255])
        mask = cv2.inRange(frame, lower_red, upper_red)
        frame_mask = cv2.bitwise_and(frame, frame, mask=mask)
        frame = cv2.cvtColor(frame_mask, cv2.COLOR_BGR2GRAY)

        if cv2.countNonZero(frame) / (frame.shape[1] * frame.shape[0]) < 0.01:
            continue

        frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        with open(os.path.join(src_path, file.replace(".png", ".json")), "r") as f:
            data = json.load(f)

        steering = data["truckFloat"]["gameSteer"]

        cv2.imwrite(os.path.join(dst_path, file), frame, [cv2.IMWRITE_PNG_COMPRESSION, 9])

        with open(os.path.join(dst_path, file.replace(".png", ".txt")), "w") as f:
            f.write(str(steering))