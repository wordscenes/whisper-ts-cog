#!/usr/bin/env python

from pathlib import Path
import sys

# append project directory to path so predict.py can be imported
sys.path.append('.')

from predict import Predictor

# Running prediction once will trigger the download of the model
p = Predictor()
p.setup()
p.predict(audio_path=Path('testing-1-2-3.mp3'), language='en')
