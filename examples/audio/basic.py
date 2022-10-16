import sys 
sys.path.append('../..')

from ml_pipeline.stream import Stream
from ml_pipeline.pipeline import Pipeline
from ml_pipeline.models import Models

from processors.audio.transcription.transcription import Transcription

# Init the models
models = Models({
  "models": {
    "transcribe": {
      "model": "audio.transcription",
      "config": {
        "size": "small"
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
    "audio": {
      "name":   "mic",
      "device": "pulse",
      "rate":   16000,
      "block":  512
    }
  }
})
stream.init()

# Create the processor
transcribe_processor = Transcription(model=models.get("transcribe"))
# Create the pipeline
transcribe_pipeline = Pipeline(processor=transcribe_processor, order="FIFO")

# Connect the pipeline to the mic audio stream
stream.connect("mic", transcribe_pipeline)