import os.path
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

from bs4 import BeautifulSoup
from .utlilts import midi_to_block, handle_uploaded_file, audio_to_midi
from .forms import UploadFileForm
from django.conf import settings
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
    midi_to_block(midi_path, "templates/" + midi_template)

    return render(request, midi_template)


def upload_audio(request):
    if request.method == "GET":
        form = UploadFileForm()
        return render(request, "upload.html", {"form": form})

    else:
        file = request.FILES["file"]
        file_url = handle_uploaded_file(file)
        file_name = file.name.split(".")[0]
        media = settings.MEDIA_ROOT
        audio_to_midi(media+"/"+file.name, "data/midi/"+file_name+".midi")
        song = Song(title=file_name)
        song.save()

        return redirect(f"/song/{song.id}", request)
