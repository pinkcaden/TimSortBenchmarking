import json
from data import VideoDataGenerator
config_data = json.load(open("config.json"))
print(config_data)

produced_arrays = [[]]

for video in config_data["input"]["video-files"]:

        matrix = VideoDataGenerator.get_frames_brightnesses("video-files/"+video,
        config_data["input"]["sampling"]["arrayCount"],
        config_data["input"]["sampling"]["arraySize"])
        for n in matrix:
            produced_arrays.append(n)

print(produced_arrays)