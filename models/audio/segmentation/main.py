import whisper
import datetime
import torch
import pyaudio
import wave

from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-segmentation")

class Model:
  def __init__(self, config):
    self.config = config
  
  def inference(self, filename):
    output = pipeline(filename)
    cues = []
    for turn, _, speaker in output.itertracks(yield_label=True):
      if len(cues)==0:
        cues.append({"start": turn.start, "end": turn.end, "speaker": speaker})
      else:
        prev = cues[-1]
        if prev["speaker"] == speaker:
          cues[-1]["end"] = turn.end
        else:
          cues.append({"start": turn.start, "end": turn.end, "speaker": speaker})
    return cues