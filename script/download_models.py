#!/usr/bin/env python

import sys
from cog import Path

# append project directory to path so predict.py can be imported
sys.path.append('.')

from predict import Predictor

# Running prediction once will trigger the download of the model
p = Predictor()
p.setup()

# Running predictions to download the denoiser models (annoying need to respecify args because when called directly, all the arguments are just FieldInfos)
p.predict(audio_path=Path('testing-1-2-3.mp3'), mode='transcribe', denoiser='demucs', language='en', aligner='new', initial_prompt='', best_of=5, beam_size=5, regroup=True, vad=True, suppress_arabic_numerals=True, suppress_pronounceable_symbols=True)
# p.predict(audio_path=Path('testing-1-2-3.mp3'), mode='transcribe', denoiser='dfnet', language='en', aligner='new', initial_prompt='', best_of=5, regroup=True, vad=True, suppress_arabic_numerals=True, suppress_pronounceable_symbols=True)
# p.predict(audio_path=Path('testing-1-2-3.mp3'), mode='transcribe', denoiser='noisereduce', language='en', aligner='new', initial_prompt='', best_of=5, regroup=True, vad=True, suppress_arabic_numerals=True, suppress_pronounceable_symbols=True)