import cv2
import numpy as np

video_path = "video-data/gilbert_in_chair.mp4"

cap = cv2.VideoCapture(video_path)

print(cap)
brightness_values = []
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale and get mean brightness
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    brightness_values.append(brightness)

cap.release()
legit = []
for n in brightness_values:
    legit.append(float(n))
print(legit)
print(len(brightness_values))