# Speaker Segmentation

https://huggingface.co/pyannote/speaker-segmentation

## Specs

### Input

- filename: a wav filename

### Output

- List of objects:
  - start (float, in seconds)
  - end (float, in seconds)
  - speaker (string)