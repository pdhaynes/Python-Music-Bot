import discord
import random
import asyncio
import time

class DiscordMusic:
  def __init__(self):
    self.isPlaying = False
    self.isJestersCurseActive = False
    self.canSkipMusic = True
    self.currentMusicTask = None
    self.lastSongPlayTime = None

    self.queue = []

  async def check_for_channel(self, ctx: discord.Interaction):
    try:
      channel = ctx.user.voice.channel
      return channel
    except AttributeError:
      return await ctx.response.send_message("You must be connected to a voice channel.")
    
  async def check_for_jester(self, ctx: discord.Interaction):
    if ctx.user.name == "reemsreg":
      return True
    else:
      return False

  async def roll_jesters_curse(self):
    target_int = random.randint(1,3)
    if target_int == 1:
      return True
    else:
      return False
    
  async def check_song_length(self, ctx: discord.Interaction, song):
    if ctx.user.name == "sirkillurass":
      return True
    else:
      if song.length > 600:
        return await ctx.response.send_message("You cannot play songs longer than 10 minutes.")
      else:
        return True
    
  async def play(self, ctx: discord.Interaction, channel, song):
    self.isPlaying = True
    self.lastSongPlayTime = time.time()
    guild = ctx.guild

    if song.jesters_curse:
      self.isJestersCurseActive = True
    else:
      self.isJestersCurseActive = False

    remainder = song.length % 60
    min = round(((song.length - remainder) / 60), 1)
    sec = song.length % 60

    await ctx.followup.send(f"Playing {song.title} by {song.author}.\n Duration {int(min)}m {sec}s")

    if not guild.voice_client:
      await channel.connect()

    guild.voice_client.play(discord.FFmpegPCMAudio(song.path))
    self.currentMusicTask = await asyncio.sleep(song.length + 1)
    self.queue.pop(0)
    if len(self.queue) > 0:
      await self.play(ctx, channel, self.queue[0])

    elif self.queue == []:
      self.isPlaying = False
      await self.timeout_check(ctx)

  def add_to_queue(self, song):
    self.queue.append(song)
    print(f"Added {song.title} to queue.")

  def remove_from_queue(self, index):
    return self.queue.pop(index)

  async def timeout_check(self, ctx: discord.Interaction):
    print("[Timeout Check] Starting check")
    guild = ctx.guild

    if self.lastSongPlayTime != None:
      elapsed_time = time.time() - self.lastSongPlayTime
      if elapsed_time > 600:
        print("[Timeout Check] More than 10 minutes have passed since a played song, disconnecting bot.")
        if guild.voice_client:
          return await guild.voice_client.disconnect()
      
      print(f"[Timeout Check] Time since last song: {round(elapsed_time, 1)}s")
    await asyncio.sleep(60 * 3) # 3 minutes
    await self.timeout_check(ctx)