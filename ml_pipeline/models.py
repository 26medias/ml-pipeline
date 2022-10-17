import importlib
import time

import threading
from queue import  Queue

import sys 
sys.path.append('../..')

class Models:
  def __init__(self, config={}):
    self.config = config
    self.models = {}
  
  def init(self):
    print("Loading the models...")
    for name in self.config["models"]:
      print("- Loading "+self.config["models"][name]["model"])
      lib = importlib.import_module("models."+self.config["models"][name]["model"]+".main")
      instance = getattr(lib, "Model")(self.config["models"][name]["config"], )
      self.models[name] = {
        "model": instance,
        "config": self.config["models"][name]["config"]
      }
      print("- ✓ "+self.config["models"][name]["model"])

  def get(self, name):
    return self.models[name]