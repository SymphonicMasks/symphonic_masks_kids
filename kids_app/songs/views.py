import os.path
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

from bs4 import BeautifulSoup

from django.shortcuts import render, redirect
from .models import Song


def index(request):
    if "song" in list(request.GET.keys()):
        song_id = request.GET["song"][0]
        return redirect(f"song/{song_id}", context={})

    songs = Song.objects.all()
    context = {"songs": songs}
    return render(request, "index.html", context=context)


def view_song(request, song_id: int):
    song = Song.objects.get(pk=song_id)
    midi_path = song.midi_path
    midi_template = f"songs/{song.title}.html"
    pm = PrettyMIDI(midi_path)
    pm.estimate_beat_start()
    plotter = Plotter()
    plotter.save(pm, f"templates/" + midi_template)
    if not os.path.exists(f"templates/" + midi_template):

        with open(f"templates/" + midi_template, "r") as f:
            html_doc = f
            soup = BeautifulSoup(html_doc, "html.parser")
            soup.find('head').decompose()
            soup.html.unwrap()
            soup.body.unwrap()

        for div in soup.find_all("div", {'class': 'sidebar'}):
            div.decompose()
        with open(f"templates/" + midi_template, "w") as f:
            f.write(
                '{% extends "../main.html" %}' +
                '{% block song_mid %}' +
                str(soup) +
                '{% endblock %}'
            )
    return render(request, midi_template)
