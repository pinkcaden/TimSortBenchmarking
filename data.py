from argparse import ArgumentTypeError

import cv2
import numpy as np

class FrameData:

    @staticmethod
    def get_frame_data(frame, data_types: list[str]):
        ret = {}
        for data_type in data_types:
            match data_type:
                case "brightness":
                    ret["brightness"] = (float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))))
                case _:
                    raise ArgumentTypeError("Possible Data types are: ")
        return ret

class VideoDataGenerator:
    _buffer = {}
    _settings_complete = False
    _chunk_size = None
    _list_size = None
    _frame_index = None
    _data_types = []
    _skip_values = []
    def __init__(self, video_path: str, chunk_term_count):
        self._video_path = video_path
        self._capture = cv2.VideoCapture(video_path)
        self._frame_count = self._capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self._chunk_size = chunk_term_count

    def __iter__(self):
        if not self._settings_complete:
            raise RuntimeError('Settings not complete')
        self._settings_complete = False
        self._frame_index = 0

        for data_type in self._data_types:
            self._buffer[data_type] = {}
            for skip_value in self._skip_values:
                self._buffer[data_type][skip_value] = []
        return self

    def __next__(self):

        chunk = []
        while len(chunk) < self._chunk_size:


            has_next, frame = self._capture.read()


            frame_data = FrameData.get_frame_data(frame, self._data_types)
            for data_type, val in  frame_data.items():
                for skip_value in self._skip_values:
                    if self._frame_index % skip_value == 0:
                        if len(self._buffer[data_type][skip_value]) < self._list_size:
                            self._buffer[data_type][skip_value].append(val)
                        else:
                            print("bad")
                            return chunk
                chunk.append(self._buffer[data_type])
        return chunk


    def set_capture_settings(self, list_size: int, skip_values: list[int], data_types: list[str]):
        self._list_size = list_size
        self._data_types = data_types
        self._settings_complete = True
        self._skip_values = skip_values

class ArrayMetrics:
    def __init__(self, array):
        self._array = array