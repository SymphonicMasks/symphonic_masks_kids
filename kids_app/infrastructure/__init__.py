from pathlib import Path

from .audio_process.pitch_detection import BasicPitcher
from .sheet_music.score_generation import SheetGenerator

basic_pitcher = BasicPitcher(Path("data/midi/temp.midi"))
music21_renderer = SheetGenerator([0.25, 0.5, 1, 2, 3, 4], Path("data/xml/temp.xml"))
