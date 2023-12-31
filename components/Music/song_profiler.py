# A class solely for creating song 
# objects that the bot uses to 
# play songs.
class SongProfiler:
  def __init__(self, title, path, author, length):
    self.title = title
    self.path = path
    self.author = author
    self.length = length
    self.jesters_curse = False

  def __repr__(self) -> str:
    return str(self.title)