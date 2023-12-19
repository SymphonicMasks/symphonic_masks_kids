import os.path
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

from bs4 import BeautifulSoup


def midi_to_block(midi_path: str, target_path):
    pm = PrettyMIDI(midi_path)
    pm.estimate_beat_start()
    plotter = Plotter()
    plotter.save(pm, target_path)

    with open(target_path, "r") as f:
        html_doc = f
        soup = BeautifulSoup(html_doc, "html.parser")
        soup.find('head').decompose()
        soup.html.unwrap()
        soup.body.unwrap()

    with open(target_path, "w") as f:
        f.write(
            '{% extends "../main.html" %}\n' +
            '{% block song_midi %}' +
            str(soup).replace("<!DOCTYPE html>", "") +
            '{% endblock %}'
        )


