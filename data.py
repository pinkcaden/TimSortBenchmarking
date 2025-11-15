



import cv2
import numpy as np

video = "video-data/gilbert_in_chair.mp4"


class VideoDataGenerator:
    def __init__(self, video_path):
        self._video_path = video_path
        self._capture = None
        self._last_frame = 0


    def get_frames_brightnesses(self, count):
        self._capture = cv2.VideoCapture(self._video_path)
        self._capture.set(cv2.CAP_PROP_POS_FRAMES, self._last_frame)
        ret = []
        for i in range(count):
            has_next, frame = self._capture.read()
            if not has_next: break
            ret.append(
                float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))))
        self._capture.release()
        self._last_frame += count
        return ret

    def get_all_frames_brightnesses(self, list_count, list_size):
        self._capture = cv2.VideoCapture(self._video_path)
        ret = []
        no_frames = False
        for i in range(list_count):
            if no_frames: break
            i_list = []
            for j in range(list_size):
                has_next, frame = self._capture.read()
                if not has_next: break
                i_list.append(float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))))
            ret.append(i_list)
        self._capture.release()
        return ret



