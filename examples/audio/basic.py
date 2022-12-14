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
      "block":  1024
    }
  }
})
stream.init()

# Create the processor
segmentation_processor  = Segmentation(stream=stream, models=models)

def display(name, data):
  print("--->", name, data)

# Create the pipelines
segmentation_pipeline  = Pipeline(processor=segmentation_processor, order="FIFO")

# Connect the pipeline to the mic audio stream
stream.connect("mic", segmentation_pipeline)

segmentation_pipeline.connect(display, True)