import json

from cog import BasePredictor, Path, Input
import stable_whisper


class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.model = stable_whisper.load_model('large-v2')

    def predict(self,
            audio_path: Path = Input(description="Audio to transcribe"),
            language: str = Input(default="en", description="Language to transcribe"),
    ) -> Path:
        result = self.model.transcribe(
            str(audio_path),
            language=language,
            demucs=True,
            regroup=True,
            temperature_increment_on_fallback=0.2,
            # **decode_options
            beam_size=5,
            best_of=5,
            )
        output = json.dumps(result, allow_nan=True)
        return output
