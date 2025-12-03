
import cv2
import numpy as np

class FrameData:

    @staticmethod
    def get_frame_data(frame, data_types: list[str]):
        ret = {}
        r, g, b = cv2.split(frame)
        for data_type in data_types:
            match data_type:
                case "brightness":
                    ret["brightness"] = (float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))))
                case "brightness_deviation":
                    ret["brightness_deviation"] = (float(np.std(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))))
                case "red":
                    ret["red"] = (float(np.mean(r)))
                case "green":
                    ret["green"] = (float(np.mean(g)))
                case "blue":
                    ret["blue"] = (float(np.mean(b)))
                case _:
                    raise RuntimeError("Possible Data types are: ")
        return ret

class VideoDataGenerator:
    _buffer = {}
    _settings_complete = False
    _chunk_size = None
    _list_size = None
    _frame_index = None
    _data_types = []
    _skip_values = []
    def __init__(self, video_path: str, chunk_term_count: int):
        self._video_path = video_path
        self._capture = cv2.VideoCapture(video_path)
        self._frame_count = self._capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self._chunk_size_max = chunk_term_count

    def __iter__(self):
        if not self._settings_complete:
            raise RuntimeError('Settings not complete')
        self._settings_complete = False
        self._frame_index = 0
        self._has_next = True

        for data_type in self._data_types:
            self._buffer[data_type] = {}
            for skip_value in self._skip_values:
                self._buffer[data_type][skip_value] = []
        return self

    def __next__(self):
        if not self._has_next: raise StopIteration
        chunk = []
        chunk_size = 0
        while chunk_size < self._chunk_size_max:


            self._has_next, frame = self._capture.read()
            if not self._has_next:
                for data_type in self._data_types:
                    for skip_value in self._skip_values:
                        chunk.append(self._buffer[data_type][skip_value])
                return chunk

            frame_data = FrameData.get_frame_data(frame, self._data_types)
            for data_type, val in  frame_data.items():
                for skip_value in self._skip_values:
                    if self._frame_index % skip_value == 0:
                        list_size = len(self._buffer[data_type][skip_value])
                        if list_size < self._list_size:
                            self._buffer[data_type][skip_value].append(val)
                        else:
                            chunk_size += list_size
                            chunk.append(self._buffer[data_type][skip_value])
                            self._buffer[data_type][skip_value] = []
            self._frame_index += 1
        return chunk


    def set_capture_settings(self, list_size: int, skip_values: list[int], data_types: list[str]):
        self._list_size = list_size
        self._data_types = data_types
        self._settings_complete = True
        self._skip_values = skip_values

