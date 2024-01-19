import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from pretty_midi import pretty_midi
from music21 import environment, stream
from music21.note import Note


class SheetGenerator:
    def __init__(self, fractions: List[float], default_path: Path):
        self.fractions = fractions
        self.default_path = default_path
        us = environment.UserSettings()
        us_path = us.getSettingsPath()
        if not os.path.exists(us_path):
            us.create()

        us['musescoreDirectPNGPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe' # describe in .env
        us['musicxmlPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'

    def _get_notes_from_midi(self, midi_data: pretty_midi.PrettyMIDI) -> List[Dict[str, Any]]:
        notes = []
        beats_per_second = midi_data.estimate_tempo() / 60
        avg_note_time = 1 / beats_per_second
        print(avg_note_time)
        for instrument in midi_data.instruments:
            for i, note in enumerate(instrument.notes):
                note_time = note.end - note.start
                if note_time / avg_note_time < 0.1 and i > 0:
                    if note.pitch == instrument.notes[i - 1].pitch:
                        instrument.notes[i - 1].end = note.end
                        continue

                note_fraction = note_time / avg_note_time
                note_fraction = min(self.fractions, key=lambda x: abs(x - note_fraction))
                name = pretty_midi.note_number_to_name(note.pitch)

                notes.append({
                    "note": name, "fraction": note_fraction
                })

        return notes

    def __call__(self, midi_data: pretty_midi.PrettyMIDI, output_path: Optional[Union[Path, str]]):
        notes = self._get_notes_from_midi(midi_data)
        stream1 = stream.Stream()
        for _note in notes:
            m21_note = Note(_note["name"], quarterLength=_note["fraction"])
            stream1.append(m21_note)

        if output_path is None:
            stream1.write('musicxml', fp=output_path)
            output_path = self.default_path

        midi_data.write(output_path)

        return midi_data
