import copy
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

import pretty_midi
from music21 import stream, chord, converter
from music21.note import Note


@dataclass
class MusicSubmission:
    original_stream: stream.Stream
    user_notes: List[pretty_midi.Note]
    tempo: int
    viz_path: str

    def create_skeleton(self) -> Tuple[List[str], List[float]]:
        stream_notes = self.original_stream.notes
        fractions = []
        original_notes = []
        for note in stream_notes:
            if note.isRest:
                continue
            original_notes.append(note.nameWithOctave)
            fractions.append(note.quarterLength)

        return original_notes, fractions

    def make_viz(self, make_svg: bool = False):
        original_notes, fractions = self.create_skeleton()
        stream_error = copy.deepcopy(self.original_stream)

        notes_in_one_sec = self.tempo / 60
        one_time = round(1 / notes_in_one_sec, 2)
        name = pretty_midi.note_number_to_name(self.user_notes[0].pitch)

        results = []

        while name != original_notes[0]:
            self.user_notes.pop(0)
            name = pretty_midi.note_number_to_name(self.user_notes[0].pitch)

        for i, _note in enumerate(self.user_notes):
            if i >= len(original_notes):
                break

            error = None
            name = pretty_midi.note_number_to_name(_note.pitch)
            note_time = _note.end - _note.start
            note_fraction = note_time / one_time

            if note_fraction < 0.1:
                print("continue if < 0.2", note_fraction)
                continue

            if name != original_notes[i]:
                if i + 1 < len(self.user_notes):
                    next_name = pretty_midi.note_number_to_name(self.user_notes[i + 1].pitch)

                    if next_name == original_notes[i]:
                        continue

                    elif i + 1 < len(original_notes):
                        if name == original_notes[i + 1]:
                            error = f"DUR_{note_fraction != fractions[i]}"
                            stream_error.notes[i].style.color = "yellow"
                            results.append({"index": i, "note": name, "duration": note_fraction, "error": error})

                            continue
                if i > 0:
                    prev_name = pretty_midi.note_number_to_name(self.user_notes[i - 1].pitch)
                    if prev_name == name:
                        continue
                error = "NOTE"
                wrong_note = Note(name, quarterLength=fractions[i])
                wrong_note.style.color = "red"

                orig_note = stream_error.notes[i]
                orig_note.style.color = "green"

                chord_notes = [orig_note, wrong_note]
                chord_element = chord.Chord(chord_notes)

                stream_error.replace(stream_error.notes[i], chord_element)

            elif note_fraction != fractions[i]:
                error = f"DUR_{note_fraction != fractions[i]}"
                stream_error.notes[i].style.color = "yellow"

            results.append({"index": i, "note": name, "duration": note_fraction, "error": error})

        stream_error.write('musicxml', fp=self.viz_path)
        if make_svg:
            svg = self.viz_path.replace(".xml", ".pdf")
            conv = converter.subConverters.ConverterLilypond()
            conv.write(stream_error, fmt='lilypond', fp=svg, subformats=['pdf'])

        return results
