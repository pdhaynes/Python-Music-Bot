import json
import discord

class SocialCreditHandler:
  def __init__(self):
    self.file_path = "storage\\data\\"
    self.file_name = "socialcredit.json"
    self.data = None

  async def add_credit(self, user_id, credit_amt):
    await self.intakeData()
    user_name = self.data["users"][user_id]["name"]
    if user_id in self.data["users"]:
      user_credits = self.data["users"][user_id]["credit"]
      self.data["users"][user_id]["credit"] = user_credits + credit_amt
      resulting_credits = self.data["users"][user_id]["credit"]
    else:
      self.data["users"][user_id]["credit"] = 1000 + credit_amt
      resulting_credits = self.data["users"][user_id]["credit"]
    await self.exportData()
    print(f"Added {credit_amt} credits to {user_name}.\nResulting credit: {resulting_credits}")
    return f"Added {credit_amt} credits to {user_name}.\nResulting credit: {resulting_credits}"

  async def subtract_credit(self, user_id, credit_amt):
    await self.intakeData()
    user_name = self.data["users"][user_id]["name"]
    if user_id in self.data["users"]:
      user_credits = self.data["users"][user_id]["credit"]
      self.data["users"][user_id]["credit"] = user_credits - credit_amt
      resulting_credits = self.data["users"][user_id]["credit"]
    else:
      self.data["users"][user_id]["credit"] = 1000 - credit_amt
      resulting_credits = self.data["users"][user_id]["credit"]
    await self.exportData()
    print(f"Removed {credit_amt} credits from {user_name}.\nResulting credit: {resulting_credits}")
    return f"Removed {credit_amt} credits from {user_name}.\nResulting credit: {resulting_credits}"

  async def first_time_setup(self, user_list):
    await self.intakeData()
    for user in user_list:
      user_id = user["id"]
      user_name = user["name"]
      if user_id not in self.data["users"]:
        self.data["users"][user_id] = {"name": user_name, "credit": 1000}
    await self.exportData()
    return "First time setup completed successfully."

  async def return_credit(self, user_id):
    await self.intakeData()
    user_id = str(user_id)
    if user_id in self.data["users"]:
      credit_amt = self.data["users"][user_id]["credit"]
    user_name = self.data["users"][user_id]["name"]
    await self.exportData()
    return f"User {user_name} has {credit_amt} social credits."

  async def intakeData(self):
    with open(self.file_path + self.file_name, 'r') as file:
      dictionary = json.load(file)

    self.data = dictionary

  async def exportData(self):
    with open(self.file_path + self.file_name, 'w') as file:
      data = json.dump(self.data, file, indent=3)

    self.data = None