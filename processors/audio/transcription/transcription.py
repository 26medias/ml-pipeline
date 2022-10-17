import pyaudio
import wave
import os

class Transcription:
  def __init__(self, stream, models):
    self.stream = stream
    self.models = models
    self.model = self.models.get("transcribe")["model"]
    self.configs = {}
    self.buffer = []
    self.c = 0

  def process(self, pipeline, data):
    response = self.model.inference(data["data"]["filename"])
    pipeline.output({
      "name": data["name"],
      "data": {
        "timestamp": data["data"]["timestamp"],
        "speaker": data["data"]["speaker"],
        "text": response
      }
    })
    os.remove(data["data"]["filename"])