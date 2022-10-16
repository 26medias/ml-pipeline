import importlib
import time

import threading
from queue import  Queue

import sys 
sys.path.append('../..')

class Pipeline:
  def __init__(self, processor, order="FIFO"):
    self.order = order
    self.processor = processor
    self.queue = Queue()
    self.thread = threading.Thread(target=self.process, args=())
    self.thread.start()
    print("Pipeline starting...")
  
  def receive(self, streamName, data):
    self.queue.put({'name': streamName, "data": data})
  
  def process(self):
    while True:
      data = self.queue.get()
      if data == "close":
        break
      self.processor.process(data)