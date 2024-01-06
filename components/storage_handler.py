import os
import time
import asyncio

class StorageHandler:
  def __init__(self):
   pass

  async def clean_up(self):
    print("[StorageHandler] Starting cleanup.")
    for root, dir, files in os.walk("storage\\music"):
      for filename in files:
        filename = os.path.join(root, filename)
        st=os.stat(filename)
        age=(time.time()-st.st_mtime)     

        age_in_hours = age / 60 / 60

        if age_in_hours > 24:
          os.remove(filename)

    print("[StorageHandler] Finished cleanup, going to sleep.")
    await asyncio.sleep(60 * 60 * 4)
    await self.clean_up()