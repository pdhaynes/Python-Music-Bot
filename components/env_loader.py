
import os
from dotenv import load_dotenv
from pathlib import Path

class LoadENV:
  def __init__(self):
    dotenv_path = Path("./secrets.env")
    load_dotenv(dotenv_path=dotenv_path)

  def get_env_vars(self):
    env_variables = []
    with open("./secrets.env") as env_file:
      lines = env_file.readlines()
      for tokens in lines:
        env_variables.append(tokens.split("=")[0])

    out_dict = {}
    for var in env_variables:
      value = os.getenv(var)
      out_dict.update({var: value})

    return out_dict
  
my_load_env = LoadENV()