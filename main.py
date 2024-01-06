import discord
import discord.ext
import os

from dotenv import load_dotenv
from discord import app_commands
from components.Discord.discord_commands import Commands
from components.storage_handler import StorageHandler
from discord.ext.commands import has_permissions
from components.Discord.admin_gui import AdminGUI

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
storagehandler = StorageHandler()
#admingui = AdminGUI()

load_dotenv(dotenv_path="secrets.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

@client.event
async def on_ready():
  sync_status = await tree.sync()
  for command in sync_status:
    print(f"Synced {command.name} command.")

  print("Bot started.")
  #await admingui.main()
  await storagehandler.clean_up() 

@tree.command(name="play", description="Play music.")
async def play(ctx: discord.Interaction, link: str = None, query: str = None):
  await Commands.main_music(ctx, link, query)

@tree.command(name="skip", description="Skip songs.")
async def skip(ctx: discord.Interaction, songnumber: str=None):
  await Commands.skip(ctx, songnumber)

@tree.command(name="queue", description="View the first 5 queued songs.")
@app_commands.choices(choices=[app_commands.Choice(name="Queue length", value="qlength"),
                               app_commands.Choice(name="List queue", value="listq")])
async def queue(ctx: discord.Interaction, choices: app_commands.Choice[str]):
  await Commands.queue(ctx, choices)

@tree.command(name="kill", description="Disconnect the bot and stop all music.")
@has_permissions(administrator=True)
async def kill(ctx: discord.Interaction):
  await Commands.kill(ctx)

if __name__ == "__main__":
  client.run(BOT_TOKEN)