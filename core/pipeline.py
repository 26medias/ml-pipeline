import importlib
import time

import threading
from queue import  Queue

import sys 
sys.path.append('../..')

class Pipeline:
  def __init__(self, config={}):
    self.config = config
    self.callbacks = {}
    self.streams = {}
    print("Pipeline starting...")

  def init(self):
    for key in self.config["stream"]:
      print(">", key)
      self.createStream(key, self.config["stream"][key])
  
  def createStream(self, name, config):
    lib = importlib.import_module("streams."+name+".main")
    instance = getattr(lib, "Stream")(self, config)
    self.streams[config["name"]] = {
      "config": instance,
      "stream": lib,
      "queue":  Queue(),
      "thread": threading.Thread(target=instance.stream, args=(config["name"],))
    }
    if config["name"] not in self.callbacks:
      self.callbacks[config["name"]] = []
    self.streams[config["name"]]["thread"].start()

  def listen(self, name, callback):
    self.callbacks[name].append(callback)
  
  def broadcast(self, name, data):
    if name in self.callbacks and len(self.callbacks[name])>0:
      for fn in self.callbacks[name]:
        fn(name, data)