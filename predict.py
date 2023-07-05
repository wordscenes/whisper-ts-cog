import json

from cog import BasePredictor, Path, Input
import stable_whisper
import numpy as np

temperature_increment_on_fallback=0.2


class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.model = stable_whisper.load_model('large-v2')
        # --temperature_increment_on_fallback is only supported in the stable-ts
        # CLI, not in the API, so we copy the logic here to get the same behavior
        self.temperature = tuple(np.arange(0, 1.0 + 1e-6, temperature_increment_on_fallback))

    def predict(self,
            audio_path: Path = Input(description="Audio to transcribe"),
            language: str = Input(default="en", description="Language to transcribe"),
    ) -> Path:
        result = self.model.transcribe(
            str(audio_path),
            language=language,
            demucs=True,
            regroup=True,
            # **decode_options
            beam_size=5,
            best_of=5,
            )
        output = json.dumps(result, allow_nan=True)
        return output
