import importlib
import time

import threading
from queue import  Queue

import sys 
sys.path.append('../..')

class Stream:
  def __init__(self, config={}):
    self.config = config
    self.callbacks = {}
    self.streams = {}
    print("Stream starting...")

  def init(self):
    for name in self.config["streams"]:
      print(">", name)
      config = self.config["streams"][name]
      self.createStream(name, config)
  
  def createStream(self, name, config):
    lib = importlib.import_module("streams."+config["type"]+".main")
    instance = getattr(lib, "Stream")(self, config)
    self.streams[name] = {
      "config": config,
      "stream": instance,
      "queue":  Queue(),
      "thread": threading.Thread(target=instance.stream, args=(name,))
    }
    if name not in self.callbacks:
      self.callbacks[name] = []
    self.streams[name]["thread"].start()

  def listen(self, name, callback):
    self.callbacks[name].append(callback)

  def connect(self, name, pipeline):
    self.listen(name, pipeline.receive)
  
  def broadcast(self, name, data):
    if name in self.callbacks and len(self.callbacks[name])>0:
      for fn in self.callbacks[name]:
        fn(name, data)