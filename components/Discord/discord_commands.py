import discord
from components.Discord.discord_music import DiscordMusic
from components.Music.yt_downloader import YTDownloader
import urllib.request
import re

Music = DiscordMusic()
YTDownload = YTDownloader()

class Commands:
  async def main_music(ctx: discord.Interaction, link: str = None, query:str = None):
    if link != None and query != None:
      return await ctx.response.send_message("Submit a link or a query, not both.")
    
    channel_result = await Music.check_for_channel(ctx)
    if type(channel_result) == discord.channel.VoiceChannel:
      channel = channel_result
    else:
      return channel_result      

    guild = ctx.guild
    
    await ctx.response.defer(ephemeral=True)

    if link != None:
      linkIsValid = await YTDownload.check_for_valid_link(link)
      if not linkIsValid:
        return await ctx.response.send_message("Automatic checks determined the submitted link was not valid, please try again.")
      song = await YTDownload.download_song_by_link(link)

    if query != None:
      query = query.replace(" ", "%20")
      html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
      video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", html.read().decode())
      link = "https://ww.youtube.com/watch?v=" + video_ids[0]
      song = await YTDownload.download_song_by_link(link)

    jester_check = await Music.check_for_jester(ctx)
    if jester_check:
      enact_jesters_curse = await Music.roll_jesters_curse()
      if enact_jesters_curse:
        print("[Jester's Curse] Reece lost against the odds.")
        await ctx.followup.send("The Jester's Curse!")
        song = await YTDownload.download_song_by_link("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        song.jesters_curse = True
        if guild.voice_client == None:
          await channel.connect()
        if Music.isPlaying:
          Music.add_to_queue(song)
          return await ctx.followup.send("Song added to queue.")
        else:
          Music.add_to_queue(song)
          return await Music.play(ctx, channel, song)
      else:
        print("Reece beat the odds, playing his song.")
        song = await YTDownload.download_song_by_link(link)

    length_check = await Music.check_song_length(ctx, song)
    if type(length_check) == bool:
      pass
    else:
      return length_check

    if Music.isPlaying:
      Music.add_to_queue(song)
      await ctx.followup.send(f"Added {song.title} by {song.author} to queue.\n")
    else:
      Music.add_to_queue(song)
      await Music.play(ctx, channel, song)

  async def skip(ctx: discord.Interaction, song_index: str):
    channel_result = await Music.check_for_channel(ctx)
    if type(channel_result) == discord.channel.VoiceChannel:
      channel = channel_result
    else:
      return channel_result

    if song_index != None:
      try:
        song_index = int(song_index)
      except:
        return await ctx.response.send_message("Please submit a valid number.")
    
      if song_index - 1 > len(Music.queue):
        return await ctx.response.send_message("Number entered is larger than amount of songs in queue, try again.")

    guild = ctx.guild
    
    await ctx.response.defer(ephemeral=True)

    if Music.queue == []:
      return ctx.followup.send(f"No songs available to skip.")
    
    if song_index == None or song_index == 1:
      song_index = 0
    else:
      song_index = song_index - 1

    if Music.isJestersCurseActive:
      return await ctx.followup.send("Sorry, this song is affected by the Jester's Curse, and as a result you can not skip it.")
    else:
      if song_index == 0:
        guild.voice_client.stop()
        if len(Music.queue) > 1:
          song = Music.queue.pop(0)
          await ctx.followup.send(f"Skipped {song.title}.")
          await Music.play(ctx, channel, Music.queue[0])
      else:
        Music.isPlaying = False
        song = Music.remove_from_queue(song_index)
        return await ctx.followup.send(f"Skipped {song.title}.")
      
  async def queue(ctx: discord.Interaction, choices: discord.app_commands.Choice[str]):
    if choices.value == "listq":
      if len(Music.queue) == 0:
        return await ctx.response.send_message("No songs in queue.") 
      #print(len(Music.queue) / 5)
      first_five_songs = [song for song in Music.queue[:5]]
      return_text = []
      for index, song in enumerate(first_five_songs):
        return_text.append(f"{index + 1}: {song.title} by {song.author}\n")
      return_text = "".join(return_text)
      return await ctx.response.send_message(return_text)
    
    elif choices.value == "qlength":
      if len(Music.queue) == 0:
        return await ctx.response.send_message(f"There are currently no songs queued.")
      else:
        return await ctx.response.send_message(f"There are currently {len(Music.queue)} songs queued.")
      
  async def kill(ctx: discord.Interaction):
    if ctx.user.name != "sirkillurass":
      return await ctx.response.send_message("Who do you think you are.")    
    
    guild = ctx.guild

    channel_result = await Music.check_for_channel(ctx)
    if type(channel_result) == discord.channel.VoiceChannel:
      channel = channel_result
    else:
      return channel_result      

    if guild.voice_client:
      await guild.voice_client.disconnect()
      #guild.voice_client.stop()

    Music.queue = []
    Music.isPlaying = False
    Music.isJestersCurseActive = False

    return await ctx.response.send_message("Killed the bot.")