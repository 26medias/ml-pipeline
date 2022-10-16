import whisper
import datetime
import torch
import pyaudio
import wave

model = whisper.load_model("medium")

class Model:
  def __init__(self, config):
    self.config = config
  
  def inference(self, filename):
    result = model.transcribe(filename)
    return result["text"]