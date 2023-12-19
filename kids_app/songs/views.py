import os.path
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

from bs4 import BeautifulSoup
from .utlilts import midi_to_block


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
    midi_to_block(midi_path, "templates/"+midi_template)

    return render(request, midi_template)
