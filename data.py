import cv2
import numpy as np

class VideoDataGenerator:
    @staticmethod
    def get_frames_brightnesses(path, list_count, list_size):
        capture = cv2.VideoCapture(path)
        ret = []
        no_frames = False
        for i in range(list_count):
            if no_frames: break
            i_list = []
            for j in range(list_size):
                has_next, frame = capture.read()
                if not has_next:
                    no_frames = True
                    break
                i_list.append(float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))))
            if i_list: ret.append(i_list)
        capture.release()
        return ret



class ArrayMetrics:
    def __init__(self, array):
        self._array = array