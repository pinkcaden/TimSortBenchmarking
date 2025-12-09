import json
import socket
from datetime import datetime
import tinydb as tiny
import time

from data import VideoDataGenerator
from metrics import ArrayMetrics, EnvironmentCapture
from sorts import Term, Record, Sorts


class Multiplexer:
    def __init__(self, multiplexing_config):
        self._config = multiplexing_config


class VirtualResultsDB:
    def __init__(self, storage_config):
        self._config = storage_config
        self.db = tiny.TinyDB(storage=tiny.storages.MemoryStorage)
        self._file = open('./experiments/results.csv', 'w')
    def input(self, result):
        x = result["x"]
        if x["length"] > 100:
            res = (f"{x["kendallTau"]}, {x["runDensity"]}, "
                   f"{result["f_x"]["time"]} \n")
            self._file.write(res)
            print(res)

class ExperimentDriver:
    def __init__(self, config_path="experiment_config.json"):
        with open(config_path, 'r') as file:
            self._config = json.load(file)

        self._env_data = EnvironmentCapture.capture(self._config["environmentCaptureData"])
        self._video_config = self._config["videoData"]
        self._sort_config = self._config["sortingAnalysis"]
        self._multiplexer = Multiplexer(self._config['multiplexer'])

        self._storage_config = self._config['storage']

        path = str(
            "./" + self._storage_config.get('experimentDirectory') + "/" + (self._storage_config['experimentDBName']))
        self._experiment_db = tiny.TinyDB(path).table("experiments")

        self._results_db = VirtualResultsDB(self._storage_config)

        self.experiment_id = self._generate_experiment_id()


    def _process_video(self, video_file):
        print(f"\nProcessing video: {video_file}")

        generation_stats = {
            'arraysAccepted': 0,
            'arraysRejected': 0,
        }


        for array_size in self._video_config['arraySizes']:

            vdg = VideoDataGenerator('./video-files/'+video_file, self._video_config["chunkTermCount"])
            vdg.set_capture_settings( array_size, self._video_config["frameSkips"], self._video_config["frameDataElements"])

            for chunk in vdg:
                for array in chunk:
                    l = len(array)
                    if l < 0:
                        generation_stats['arraysRejected'] += 1
                        continue

                    metrics = ArrayMetrics.get_array_metrics(array)
                    if metrics is None:
                        generation_stats['arraysRejected'] += 1
                        continue

                    for sort in self._sort_config["sorts"]:
                        sort_stats, time_taken = self._run_sort(array, sort)
                        sort_stats["sort"] = sort
                        sort_stats["time"] = time_taken
                        sort_stats["timePerElement"] = time_taken / l

                        self._results_db.input({
                            "experimentId" : self.experiment_id,
                            "x" : metrics,
                            "f_x" : sort_stats
                        })
                        generation_stats['arraysAccepted'] += 1


        return generation_stats



    def _run_sort(self, array, algorithm):
        record = Record()
        terms = [Term(value, record) for value in array]
        start_time1 = time.perf_counter()
        # if algorithm == "timsort":
        Sorts.quick_sort(terms)
        end_time1 = time.perf_counter()
        quick_time = end_time1 - start_time1
        start_time2 = time.perf_counter()
        Sorts.tim_sort(array)
        end_time2 = time.perf_counter()
        tim_time = end_time2 - start_time2

        return record.get_counts(), tim_time / quick_time

    @staticmethod
    def _generate_experiment_id():
        hostname = socket.gethostname()[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"exp_{hostname}_{timestamp}"

    def _create_experiment_entry(self):

        experiment_entry = {
            'experimentId': self.experiment_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'in_progress',
            'config': self._config,
            'environment': self._env_data,
            'summary': {
                'videosProcessed': 0,
                'arraysAccepted': 0,
                'arraysRejected': 0,
                'startTime': datetime.now().isoformat(),
                'endTime': None
            }
        }

        self._experiment_db.insert(experiment_entry)
        print(f"Created experiment: {self.experiment_id}")
        return self.experiment_id

    def complete_experiment(self):
        exp = tiny.Query()
        self._experiment_db.update({"status": "completed"}, exp.experimentId == self.experiment_id)
        self._experiment_db.update(
            lambda d: (d['summary'].update({
                'endTime': datetime.now().isoformat()
            }) or d),
            exp.experimentId == self.experiment_id
        )

        print(f"Experiment {self.experiment_id} completed")

    def run(self):
        print("=" * 60)
        print(f"Experiment {self.experiment_id}:")
        self._create_experiment_entry()

        total_stats = {
            'videosProcessed': 0,
            'arraysAnalyzed': 0,
            'arraysRejected': 0,
            'sortsCompleted': 0
        }

        for video_file in self._video_config['videoFiles']:

                video_stats = self._process_video(video_file)

                total_stats['videosProcessed'] += 1
                total_stats['arraysAnalyzed'] += video_stats['arraysAccepted']
                total_stats['arraysRejected'] += video_stats['arraysRejected']


        print(f"Total stats: {total_stats}")
        self.complete_experiment()


driver = ExperimentDriver("experiment_config.json")
driver.run()
