import discord
import random
import asyncio

class DiscordMusic:
  def __init__(self):
    self.isPlaying = False
    self.isJestersCurseActive = False
    self.canSkipMusic = True
    self.currentMusicTask = None

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
    self.currentMusicTask = await asyncio.sleep(song.length)
    self.queue.pop(0)

  def add_to_queue(self, song):
    self.queue.append(song)
    print(f"Added {song.title} to queue.")

  def remove_from_queue(self, index):
    return self.queue.pop(index)