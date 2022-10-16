import sys 
sys.path.append('../..')

from core import pipeline

config = {
  "stream": {
    "audio": {
      "name":   "mic",
      "device": "pulse",
      "rate":   16000
    }
  }
}


def micProcessor(streamName, audio_frame):
  print("$$> ", streamName, audio_frame)


app = pipeline.Pipeline(config=config)
app.init()
app.listen("mic", micProcessor)