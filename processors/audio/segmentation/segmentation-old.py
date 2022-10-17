import pyaudio
import wave

class Segmentation:
  def __init__(self, stream, models):
    self.stream = stream
    self.models = models
    self.configs = {}
    self.buffer = []
    self.c = 0
    print("Transcription starting...")

  def process(self, pipeline, data):
    config = self.stream.config["streams"][data["name"]]
    self.buffer.append(data["data"])
    bufferLength = len(self.buffer)
    print(bufferLength)
    if bufferLength>=5:
      tempfilename = "test-rec-"+str(self.c)+".wav"
      self.saveWav(b''.join(self.buffer), tempfilename, config["rate"])
      self.c = self.c + 1
      self.buffer = []
      pipeline.output({"name": data["name"], "data": tempfilename})
    #print("received: ", data["name"], config, blockDuration, bufferDuration)
  
  def saveWav(self, data, filename, framerate):
    with wave.open(filename, 'w') as outfile:
      outfile.setnchannels(1)
      outfile.setsampwidth(2)
      outfile.setframerate(framerate)
      outfile.setnframes(int(len(data) / 2))
      outfile.writeframes(data)