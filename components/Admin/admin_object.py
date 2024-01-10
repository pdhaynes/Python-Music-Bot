import json

class AdminObject:
  def __init__(self):
    self.file_path = "storage\\data\\"
    self.file_name = "admindata.json"
    self.data = None

  async def isAdmin(self, user_id) -> bool:
    await self.intakeData()
    response = None
    if str(user_id) in self.data["admin-users"]:
      response = True
    else:
      response =  False
    await self.exportData()
    return response

  async def canSkip(self, user_id) -> bool:
    await self.intakeData()
    response = None
    if str(user_id) in self.data["cant-skip"]:
      response = False
    else:
      response = True
    await self.exportData()
  
  async def canUseBot(self, user_id) -> bool:
    await self.intakeData()
    response = None
    if str(user_id) in self.data["cant-use-bot"]:
      response = False
    else:
      response = True
    await self.exportData()
  
  async def addAdmin(self, user_id):
    #open json file, add user id to admin-users
    await self.intakeData()
    self.data["admin-users"].append(user_id)
    await self.exportData()
    print(f"Added {user_id} to admin list.")

  async def addSkipBlacklist(self, user_id):
    #open json file, add user id to cant-skip
    await self.intakeData()
    self.data["cant-skip"].append(user_id)
    await self.exportData()
    print(f"Added {user_id} to skip blacklist.")

  async def addBotBlacklist(self, user_id):
    #open json file, add user id to acant-use-bot
    await self.intakeData()
    self.data["cant-use-bot"].append(user_id)
    await self.exportData()
    print(f"Added {user_id} to bot blacklist.")

  async def removeAdmin(self, user_id):
    #open json file, remove user id from admin-users
    await self.intakeData()
    removal_index = None
    for i, user in self.data["admin-users"]:
      if user_id == user:
        removal_index = i
    log = self.data["admin-users"].pop(i)
    await self.exportData()
    print(f"Removed {log} from admin list.")

  async def removeSkipBlacklist(self, user_id):
    #open json file, remove user id from cant-skip
    await self.intakeData()
    removal_index = None
    for i, user in self.data["cant-skip"]:
      if user_id == user:
        removal_index = i
    log = self.data["cant-skip"].pop(i)
    await self.exportData()
    print(f"Removed {log} from skip blacklist.")

  async def removeBotBlacklist(self, user_id):
    await self.intakeData()
    removal_index = None
    for i, user in self.data["cant-use-bot"]:
      if user_id == user:
        removal_index = i
    log = self.data["cant-use-bot"].pop(i)
    await self.exportData()
    print(f"Removed {log} from bot blacklist.")

  async def intakeData(self):
    with open(self.file_path + self.file_name, 'r') as file:
      dictionary = json.load(file)

    self.data = dictionary

  async def exportData(self):
    with open(self.file_path + self.file_name, 'w') as file:
      data = json.dump(self.data, file, indent=3)

    self.data = None