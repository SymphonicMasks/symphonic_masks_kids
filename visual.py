from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

pm = PrettyMIDI("forest_d.midi")
pm.estimate_beat_start()
plotter = Plotter()
plotter.save(pm, "example-01.html")