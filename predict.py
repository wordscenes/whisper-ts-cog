# Predictor using the stable-whisper library with hardwired configuration that we found to work;
# TODO: copy the CLI configuration options into the API; to do this, it would be easier if all of the CLI
# options (of stable-ts) were available programmatically as well

import json
import os
import typing

from cog import BasePredictor, Path, Input
from cog.types import Weights
import stable_whisper
import numpy as np
from torch import nn

# all model files will be downloaded to this directory
MODEL_CACHE = Path(__file__).parent / 'model_cache'
temperature_increment_on_fallback = 0.2

# Not v3! See "rejected experiments" in readme
WHISPER_MODEL = 'large-v2'


def report_versions():
    print(f'Using stable-ts version {stable_whisper.__version__}')
    print('*Not* using faster-whisper')  # see "rejected experiments" in readme
    print(f'Using Whisper model {WHISPER_MODEL}')


class Predictor(BasePredictor):
    def setup(self, weights: Weights | None = None):
        """Load the model into memory to make running multiple predictions efficient"""

        # Ensure the model cache directory exists
        os.makedirs(MODEL_CACHE, exist_ok=True)

        # Ensure that demucs models are downloaded to the cache directory
        os.environ["TORCH_HOME"] = str(MODEL_CACHE)

        self.model = stable_whisper.load_model(
            WHISPER_MODEL,
            # This is supposed to make loading faster, but it results in encoding errors for Japanese
            # cpu_preload=True,
            download_root=str(MODEL_CACHE),
            device='cuda')

        # --temperature_increment_on_fallback is only supported in the stable-ts
        # CLI, not in the API, so we copy the logic here to get the same behavior
        self.temperature = tuple(np.arange(0, 1.0 + 1e-6, temperature_increment_on_fallback))

    def predict(self,
            audio_path: Path = Input(description="Audio to transcribe or align"),
            mode: str = Input(default="transcribe", choices=["transcribe", "align"], description="Mode: 'transcribe' to generate transcript, 'align' to align provided text"),
            text: str = Input(default="", description="Text to align with audio (required when mode='align')"),
            language: str = Input(default="en", description="Language to transcribe"),
            # False by default because we think it might be too aggressive and remove some voice data
            demucs: bool = Input(default=False, description="Whether to preprocess the audio track with Demucs to isolate vocals/remove noise (transcribe mode only)."),
            # Super important for reducing prediction time
            vad: bool = Input(default=True, description="Whether to use Silero VAD to generate timestamp suppression mask."),
            beam_size: int = Input(default=5, description="Number of beams in beam search, only applicable when temperature is zero (transcribe mode only)."),
            best_of: int = Input(default=5, description="Number of candidates when sampling with non-zero temperature (transcribe mode only)."),
            regroup: bool = Input(default=True, description="Whether to regroup all words into segments with more natural boundaries."),
            initial_prompt: str = Input(default="", description="Text to provide as a prompt for the first window (transcribe mode only)."),
            **_kwargs,
    ) -> str:
        report_versions()

        if mode == "align":
            if text is "":
                raise ValueError("text parameter is required when mode='align'")
            result = typing.cast(nn.Module, self.model.align)(
                str(audio_path),
                text=text,
                language=language,
                vad=vad,
                regroup=regroup,
            )
        else:  # transcribe
            result = self.model.transcribe(
                str(audio_path),
                language=language,
                demucs=demucs,
                vad=vad,
                regroup=regroup,
                beam_size=beam_size,
                best_of=best_of,
                initial_prompt=initial_prompt,
            )

        # Adapted from stable_whisper/text_output.py; original can only save to file
        if not isinstance(result, dict) and callable(getattr(result, 'to_dict')):
            result = result.to_dict()
        output = json.dumps(result, allow_nan=True, ensure_ascii=False)

        return output
