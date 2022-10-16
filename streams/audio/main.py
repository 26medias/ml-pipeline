import pyaudio
import wave

class Stream:
  def __init__(self, core, config):
    self.core = core
    self.config = config
    self.started = False
    print("Stream started")

  def getDeviceId(self, name="pulse"):
    info = self.audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
      if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        if self.audio.get_device_info_by_host_api_device_index(0, i).get('name')==name:
          return i
    return 0
  
  def getStream(self):
    index = self.getDeviceId(name=self.config["device"])
    print("Using device #"+str(index))
    stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=self.config["rate"], input=True, input_device_index = index, frames_per_buffer=self.config["rate"])
    return stream
  
  def start(self):
    if self.started==True:
      return True
    self.audio = pyaudio.PyAudio()
    self.stream = self.getStream()
    self.started = True
    return True
  
  def stop(self):
    if self.started==False:
      return True
    self.stream.stop_stream()
    self.stream.close()
    self.audio.terminate()
    self.started = False
    return True

  def record(self, duration=5):
    print("Recording for ",duration,"seconds")
    Recordframes = []
    for i in range(0, duration):
      data = self.stream.read(self.config["rate"])
      Recordframes.append(data)
    print("Recording stopped.")
    return Recordframes
  
  def save(self, recording, filename="recording.wav"):
    print("Saving ", filename)
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(1)
    waveFile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(self.config["rate"])
    waveFile.writeframes(b''.join(recording))
    waveFile.close()
    print("Saved.")
  
  def test(self):
    self.start()
    rec = self.record(5)
    self.save(rec, "test.wav")
    self.stop()
  
  def stream(self, name):
    print("----", name)
    self.start()
    while True:
      self.core.broadcast(name, self.stream.read(self.config["rate"]))