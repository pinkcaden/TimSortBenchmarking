import json
from data import VideoDataGenerator
from metrics import ArrayMetrics
# config_data = json.load(open("config.json"))
# print(config_data)
#
# produced_arrays = [[]]
#
# for video in config_data["input"]["video-files"]:
#
#         matrix = VideoDataGenerator.get_frames_brightnesses("video-files/"+video,
#         config_data["input"]["sampling"]["arrayCount"],
#         config_data["input"]["sampling"]["arraySize"])
#         for n in matrix:
#             produced_arrays.append(n)
# print(produced_arrays)

print(ArrayMetrics.count_inversions([1, 3, 5, 2, 4, 6 ] ))

vdg = VideoDataGenerator("video-files/turtle_to_ocean.mp4", 400)

vdg.set_capture_settings(100, [1,2,4,6,8], ["brightness"])

for n in vdg:
    for val in n:
        print(val)
        arr, count = ArrayMetrics.count_inversions(val)
        print(count)