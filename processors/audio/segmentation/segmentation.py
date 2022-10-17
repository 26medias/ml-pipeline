import pyaudio
import wave
import datetime
import os

class Segmentation:
  def __init__(self, stream, models):
    self.stream = stream
    self.models = models
    self.model = self.models.get("segmentation")["model"]
    self.configs = {}
    self.buffer = []

  def process(self, pipeline, data):
    config = self.stream.config["streams"][data["name"]]
    self.buffer.append(data["data"]["data"])
    bufferLength = len(self.buffer)
    if bufferLength>=10:
      tempfilename = "chunk-"+str(data["data"]["timestamp"])+".wav"
      self.saveWav(b''.join(self.buffer), tempfilename, config["rate"])
      self.split(tempfilename, data["name"], data["data"]["timestamp"], pipeline)
      self.buffer = []
      #pipeline.output({"name": data["name"], "data": tempfilename})
  
  def split(self, filename, name, timestamp, pipeline):
    cues = self.getCues(filename)
    parts = self.cutWav(filename, cues, timestamp)
    for part in parts:
      pipeline.output({"name": name, "data": part})

  def saveWav(self, data, filename, framerate):
    with wave.open(filename, 'w') as outfile:
      outfile.setnchannels(1)
      outfile.setsampwidth(2)
      outfile.setframerate(framerate)
      outfile.setnframes(int(len(data) / 2))
      outfile.writeframes(data)

  def getCues(self, filename):
    cues = []
    return self.model.inference(filename)

  def cutWav(self, filename, cues, timestamp):
    # file to extract the snippet from
    parts = []
    with wave.open(filename, "rb") as infile:
        # get file data
        framerate = infile.getframerate()
        # set position in wave to start of segment
        for n, cue in enumerate(cues):
          infile.setpos(int(cue["start"] * framerate))
          # extract data
          data = infile.readframes(int((cue["end"] - cue["start"]) * framerate))
          outname = "dialog--"+str(timestamp+cue["start"])+".wav"
          self.saveWav(data, outname, framerate)
          parts.append({
            "filename": outname,
            "timestamp": timestamp+cue["start"],
            "speaker": cue["speaker"]
          })
        os.remove(filename)
    return parts