import json
from data import VideoDataGenerator
config_data = json.load(open("config.json"))
print(config_data)

data = {}
for video in config_data["data"]["video-data"]:
    print(video)
    data[video] = VideoDataGenerator("video-data/"+video)
    print(data[video].get_frames_brightnesses(config_data["data"]["arrayCount"], config_data["data"]["arraySize"]))