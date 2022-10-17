import importlib
import time
import inspect

import threading
from queue import  Queue

import sys 
sys.path.append('../..')

class Pipeline:
  def __init__(self, processor, order="FIFO"):
    self.order = order
    self.processor = processor
    self.queue = Queue()
    self.out_queue = Queue()
    self.thread = threading.Thread(target=self.process, args=())
    self.thread.start()
    self.out_thread = threading.Thread(target=self.process_out, args=())
    self.out_thread.start()
    print("Pipeline starting...")
  
  def receive(self, streamName, data):
    self.queue.put({'name': streamName, "data": data})
  
  def process(self):
    while True:
      data = self.queue.get()
      if data == "close":
        break
      self.processor.process(self, data)

  def process_out(self):
    while True:
      data = self.out_queue.get()
      if data == "close":
        break
      if self.isFunction:
        self.outpipe(data["name"], data["data"])
      else:
        self.outpipe.receive(data["name"], data["data"])

  def connect(self, outpipe, isFunction=False):
    self.outpipe = outpipe
    self.isFunction = isFunction
  
  def output(self, data):
    self.out_queue.put(data)
