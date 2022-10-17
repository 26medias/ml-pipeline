import time
import sys 
sys.path.append('../..')

from ml_pipeline.stream import Stream
from ml_pipeline.pipeline import Pipeline
from ml_pipeline.models import Models

from processors.audio.segmentation.segmentation import Segmentation
from processors.audio.transcription.transcription import Transcription

# Init the models
models = Models({
  "models": {
    "transcribe": {
      "model": "audio.transcription",
      "config": {
        "size": "medium"
      }
    },
    "segmentation": {
      "model": "audio.segmentation",
      "config": {}
    }
  }
})
models.init()

# Init the streams
stream = Stream(config={
  "streams": {
    "mic": {
      "type":   "audio",
      "device": "pulse",
      "rate":   16000,
      "block":  512
    }
  }
})
stream.init()

# Create the processor
segmentation_processor  = Segmentation(stream=stream, models=models)
transcription_processor = Transcription(stream=stream, models=models)

def display(name, data):
  lag = time.time()-data["timestamp"]
  print(">", name, data["timestamp"], data["speaker"], data["text"])

# Create the pipelines
segmentation_pipeline  = Pipeline(processor=segmentation_processor, order="FIFO")
transcription_pipeline = Pipeline(processor=transcription_processor, order="FIFO")

# Connect the pipeline to the mic audio stream
stream.connect("mic", segmentation_pipeline)
segmentation_pipeline.connect(transcription_pipeline)


transcription_pipeline.connect(display, True)