import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

import music21.stream
import pretty_midi
from music21 import environment, stream, converter, musicxml
from music21.note import Note


class SheetGenerator:
    def __init__(self, fractions: List[float], default_path: Path):
        self.fractions = fractions
        self.default_path = default_path
        self.env = environment.Environment
        us = environment.UserSettings()
        us_path = us.getSettingsPath()
        if not os.path.exists(us_path):
            us.create()

        # us['musescoreDirectPNGPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'  # describe in .env
        # us['musicxmlPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'
        # us['lilypondPath'] = r'"C:\Program Files\lilypond-2.24.3\bin\lilypond.exe"'

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

    def generate_html_block(self,
                            output_stream: Optional[stream.Stream] = None,
                            midi_data: Optional[pretty_midi.PrettyMIDI] = None,
                            ):
        if output_stream is None:
            if midi_data is None:
                raise TypeError(" if output is not given, ")
            output_stream = self.__call__(midi_data)

        GEX = musicxml.m21ToXml.GeneralObjectExporter(output_stream)
        out = GEX.parse()
        musicxml_code = out.decode('utf-8')

        lilypond_file_path = 'data/output.ly'
        output_stream.write('lilypond', fp=lilypond_file_path)

        # Convert LilyPond to PNG using LilyPond command line tool
        output_image_path = 'data/output.png'
        self.env.run(['lilypond', '--png', '-o', output_image_path, lilypond_file_path])

        html_code = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="UTF-8">
              <meta http-equiv="X-UA-Compatible" content="IE=edge">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>Music21 Stream Rendering</title>
              <script src="https://cdnjs.cloudflare.com/ajax/libs/vexflow/1.4.21/vexflow-min.js"></script>
            </head>
            <body>
              <div id="notation"></div>
              <script>
                var vf = new Vex.Flow.Factory({"{renderer: { {elementId: 'notation'} }}"});
                var score = vf.EasyScore();
                var system = vf.System();
            
                // Parse MusicXML code
                var xmlString = '{musicxml_code}';
                var parser = new DOMParser();
                var xmlDoc = parser.parseFromString(xmlString, 'application/xml');
            
                // Render the MusicXML using VexFlow
                system.addStave({"{voices: [score.voice(score.notes(xmlDoc))]}"}).draw();
              </script>
            </body>
            </html>
            """
        with open("data/temp.html", "w") as f:
            f.write(html_code)
        return html_code

    def __call__(self, midi_data: pretty_midi.PrettyMIDI, output_path: Optional[Union[Path, str]] = None):
        notes = self._get_notes_from_midi(midi_data)
        stream1 = stream.Stream()
        for _note in notes:
            m21_note = Note(_note["note"], quarterLength=_note["fraction"])
            stream1.append(m21_note)

        if output_path is None:
            output_path = self.default_path

        stream1.write('musicxml', fp=output_path)

        return stream1
