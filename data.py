import cv2
import numpy as np

class VideoDataGenerator:
    def __init__(self, video_path):
        self._video_path = video_path

    def get_frames_brightnesses(self, list_count, list_size):
        capture = cv2.VideoCapture(self._video_path)
        ret = []
        no_frames = False
        for i in range(list_count):
            if no_frames: break
            i_list = []
            for j in range(list_size):
                has_next, frame = capture.read()
                if not has_next: break
                i_list.append(float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))))
            ret.append(i_list)
        capture.release()
        return ret



