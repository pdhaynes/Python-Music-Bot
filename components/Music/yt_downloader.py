import os
import re
from pytube import YouTube
from components.Music.song_profiler import SongProfiler

music_download_path = "storage/music/"

class YTDownloader:
  def __init__(self):
    self.restricted_chars = ["?", "/", "\\", "(", ")", "|", '"', "'"]

  async def check_for_valid_link(self, link):
    youtube_regex = r"[https.:\/\/www.youtube.com\/watch?v=[A-Z-a-z0-9]"

    youtube_match = re.match(youtube_regex, link)
    return bool(youtube_match)

  async def download_song_by_link(self, link):
    youtube_info = YouTube(link)

    title = self.clean_title(youtube_info.title.title())
    length = youtube_info.length
    author = youtube_info.author
    path = title + ".mp3"
    full_path = music_download_path + path

    if os.path.exists(full_path):
      print("Song found, skipping download.")
    else:
      try:
        YouTube(link, use_oauth=True, allow_oauth_cache=True).streams.filter(only_audio=True, subtype="webm").first().download(output_path=music_download_path, filename=path)
      except:
        YouTube(link, use_oauth=True, allow_oauth_cache=True).streams.filter(only_audio=True).first().download(output_path=music_download_path, filename=path)

    SongProfile = SongProfiler(title, full_path, author, length)
    return SongProfile

  def clean_title(self, title) -> str:
    title_chars = [char for char in title]
    char_remove = []

    for i, char in enumerate(title_chars):
      if char in self.restricted_chars:
        char_remove.append(i)

    char_remove.reverse()
    for i in char_remove:
      title_chars.pop(i)

    cleaned_title = "".join(title_chars)
    return cleaned_title