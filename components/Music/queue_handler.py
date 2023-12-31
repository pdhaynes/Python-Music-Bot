from song_profiler import SongProfiler
import json

class QueueHandler:
  def __init__(self):
    self.queue = []

  @classmethod
  def add_to_queue(self, song_profile: SongProfiler) -> None:
    self.queue.append(song_profile)
    return None

  @classmethod
  def remove_from_queue(self, index) -> None:
    self.queue.remove(index)
    return None

  @classmethod
  def return_queue(self) -> json:
    return_json = {}
    for index, song in self.queue:
      return_json.update({index: {"title": song.title, "author": song.author, "length": song.length}})

    return_json = json.dumps(return_json)
    return return_json
  
qh = QueueHandler()