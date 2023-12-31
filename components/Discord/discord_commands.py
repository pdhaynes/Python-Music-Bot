import discord
from components.Discord.discord_music import DiscordMusic
from components.Music.yt_downloader import YTDownloader

Music = DiscordMusic()
YTDownload = YTDownloader()

class Commands:
  async def main_music(ctx: discord.Interaction, link: str = None):
    channel_result = await Music.check_for_channel(ctx)
    if type(channel_result) == discord.channel.VoiceChannel:
      channel = channel_result
    else:
      return channel_result      

    #linkIsValid = await YTDownload.check_for_valid_link(link)
    #if not linkIsValid:
    #  return await ctx.response.send_message("Automatic checks determined the submitted link was not valid, please try again.")

    guild = ctx.guild
    
    await ctx.response.defer(ephemeral=True)

    jester_check = await Music.check_for_jester(ctx)
    if jester_check:
      enact_jesters_curse = await Music.roll_jesters_curse()
      if enact_jesters_curse:
        print("[Jester's Curse] Reece lost against the odds.")
        await ctx.followup.send("The Jester's Curse!")
        song = await YTDownload.download_song("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
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
        song = await YTDownload.download_song(link)
    elif link != None:
      song = await YTDownload.download_song(link)
    else:
      raise Exception("Uncaught possibility found within play functioon")

    length_check = await Music.check_song_length(ctx, song)
    if type(length_check) == bool:
      pass
    else:
      return length_check

    if Music.isPlaying:
      Music.add_to_queue(song)
    else:
      Music.add_to_queue(song)
      await Music.play(ctx, channel, song)
      #if len(Music.queue) > 1:
      #  await Music.play(ctx, channel, Music.queue[0])

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
          #song = Music.remove_from_queue(song_index)
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