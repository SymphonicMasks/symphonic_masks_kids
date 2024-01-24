import os
from pathlib import Path
from typing import List, Optional, Union, Tuple

import music21.stream
from django.conf import settings
import pretty_midi
from music21 import environment, stream
from music21.note import Note


class SheetGenerator:
    def __init__(self, fractions: List[float], pause_fractions: List[float], default_path: Path):
        self.fractions = fractions
        self.pause_fractions = pause_fractions
        self.default_path = default_path
        self.env = environment.Environment
        us = environment.UserSettings()
        us_path = us.getSettingsPath()
        if not os.path.exists(us_path):
            us.create()

        us['musescoreDirectPNGPath'] = settings.musescoreDirectPNGPath
        us['musicxmlPath'] = settings.musicxmlPath
        us['lilypondPath'] = settings.lilypondPath

    def _get_notes_from_midi(self, midi_data: pretty_midi.PrettyMIDI) -> Tuple[List[pretty_midi.Note], float]:
        notes = []
        tempo = midi_data.estimate_tempo()
        beats_per_second = tempo / 60
        avg_note_time = 1 / beats_per_second
        print(avg_note_time)
        for instrument in midi_data.instruments:
            for i, note in enumerate(instrument.notes):
                note_time = note.end - note.start
                if note_time / avg_note_time < 0.1 and i > 0:
                    if note.pitch == instrument.notes[i - 1].pitch:
                        instrument.notes[i - 1].end = note.end
                        continue
                notes.append(note)

                note_fraction = note_time / avg_note_time
                note_fraction = min(self.fractions, key=lambda x: abs(x - note_fraction))
                name = pretty_midi.note_number_to_name(note.pitch)

                notes.append({
                    "note": name, "fraction": note_fraction
                })

        return notes, tempo

    def _preprocess_notes(self, notes: List[pretty_midi.Note], tempo: float) -> stream.Stream:
        m21_notes = []
        notes_in_one_sec = tempo / 60
        one_time = round(1 / notes_in_one_sec, 2)
        stream1 = stream.Stream()

        for i, _note in enumerate(notes):
            options = self.fractions
            pause_options = self.pause_fractions

            name = pretty_midi.note_number_to_name(_note.pitch)
            rest = None
            if i + 1 < len(notes):
                next_note = notes[i + 1]

                if next_note.start < _note.end:
                    _note.end = next_note.start
                pause_fraction = (next_note.start - _note.end) / one_time
                if pause_fraction > 0.7:
                    rest_fraction = min(pause_options, key=lambda x: abs(x - pause_fraction))
                    rest = music21.note.Rest(quarterLength=rest_fraction)

            note_time = _note.end - _note.start
            note_fraction = note_time / one_time

            note_fraction = min(options, key=lambda x: abs(x - note_fraction))
            m21_note = Note(name, quarterLength=note_fraction)

            m21_notes.append(m21_note)
            stream1.append(m21_note)

            if rest is not None:
                stream1.append(rest)

        return stream1

    def __call__(self, midi_data: pretty_midi.PrettyMIDI, output_path: Optional[Union[Path, str]] = None) -> str:
        notes, tempo = self._get_notes_from_midi(midi_data)
        stream1 = self._preprocess_notes(notes, tempo)

        if output_path is None:
            output_path = self.default_path

        stream1.write('musicxml', fp=output_path)

        return str(output_path)
