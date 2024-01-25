from pathlib import Path
import os

from music21 import environment

from kids_app import settings
from .audio_process.pitch_detection import BasicPitcher
from .sheet_music.score_generation import SheetGenerator
from .sheet_music.music_submission import MusicSubmission

us = environment.UserSettings()
us_path = us.getSettingsPath()
if not os.path.exists(us_path):
    us.create()

us['musescoreDirectPNGPath'] = settings.musescoreDirectPNGPath
us['musicxmlPath'] = settings.musicxmlPath
us['lilypondPath'] = settings.lilypondPath

basic_pitcher = BasicPitcher(Path("data/midi/temp.midi"))
music21_renderer = SheetGenerator([0.5, 1, 4], [1], Path("data/xml/temp.xml"))
