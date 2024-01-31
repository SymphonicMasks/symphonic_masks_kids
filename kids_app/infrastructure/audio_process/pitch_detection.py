from pathlib import Path
from typing import Union, Optional

from basic_pitch.inference import predict


class BasicPitcher:
    def __init__(self, default_path: Path):
        self.default_path = default_path

    def __call__(self, audio_file_path: Union[Path, str], output_path: Optional[Union[Path, str]]):
        model_output, midi_data, note_events = predict(audio_file_path,
                                                       onset_threshold=0.6,
                                                       minimum_frequency=130.813,
                                                       maximum_frequency=1278.75)

        if output_path is None:
            output_path = self.default_path

        midi_data.write(output_path)

        return midi_data
