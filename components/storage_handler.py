import os
import time
import asyncio

class StorageHandler:
  def __init__(self):
    self.clean_up()

  async def clean_up(self):
    print("Starting storage cleanup.")
    for root, dir, files in os.walk("storage\music"):
      for filename in files:
        filename = os.path.join(root, filename)
        st=os.stat(filename)
        age=(time.time()-st.st_mtime)     

        age_in_hours = age / 60 / 60

        if age_in_hours > 24:
          os.remove(filename)

    asyncio.sleep(60 * 4)
    await self.clean_up()