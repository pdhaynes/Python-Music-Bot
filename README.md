This is a Discord bot that is free to use/implement in your own server.

This repo assumes that:
1. You have already created a discord bot with the required intents on the discord admin page
2. You are only using the bot in one server

If you have not already created a discord bot you intend to use this logic for, there are guides out there that will show you how to do so.
Up to this point, this bot has only been coded for my personal use in my own private Discord server, and will require additional code in order
to make it compatible with numerous servers. Feel free to go through and make those changes where needed.

This bot is "no strings attached" if you use it. Since I am coding this for my own private server and providing this publicly for free, I do not take suggestions and will
not add requested features to the bot, unless it is something I had already planned on doing and/or my server would benefit from it.

REQUIREMENTS:
1.  A created discord bot and corresponding token.
2.  A secrets.env file placed in the topmost folder structure of the bot
  - BOT_TOKEN='ThiSisAnExampLeOfTheLineNeeDedInTHeSecreTsFolDer'
3.  The following python packages installed on the host machine:
  - discord
  - py-cord
  - PyNaCl
  - os
  - dotenv
  - urllib.request
  - re
  - time
  - asyncio
  - random
  - pytube
