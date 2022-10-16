
class Transcription:
  def __init__(self, model):
    self.model = model
    print("Transcription starting...")

  def process(self, data):
    print("received: ", len(data))