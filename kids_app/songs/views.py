import os.path
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

from bs4 import BeautifulSoup
from .utlilts import midi_to_block, handle_uploaded_file, audio_to_midi
from .forms import UploadFileForm
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from .models import Song


def index(request):
    if "song" in list(request.GET.keys()):
        song_id = request.GET["song"][0]
        return redirect(f"song/{song_id}", context={})

    songs = Song.objects.all()
    form = UploadFileForm()
    context = {
        "songs": songs,
        "form": form
    }

    return render(request, "index.html", context=context)


def view_song(request, song_id: int):
    song = Song.objects.get(pk=song_id)
    context = {
        "user_input_block": None,
    }
    if request.session.has_key("user_id"):
        user_id = request.session.get("user_id")
        midi_template = f"user_midi/{user_id}/{song.title}.html"
        context = {
            "user_input_block": midi_template,
        }

    midi_path = song.midi_path
    midi_template = f"songs/{song.title}.html"
    midi_to_block(midi_path, "templates/" + midi_template)

    context["song_midi"] = midi_template

    return render(request, "main.html", context)


def upload_audio(request):
    if request.method == "GET":
        form = UploadFileForm()
        return render(request, "upload.html", {"form": form})

    else:
        file = request.FILES["file"]
        song_id = request.POST["song"]
        file_url = handle_uploaded_file(file)
        file_name = file.name.split(".")[0]
        media = settings.MEDIA_ROOT
        song = Song.objects.get(pk=song_id)

        user_id = 1
        audio_to_midi(media+"/"+file.name, "data/midi/"+file_name+".midi")
        midi_template = f"user_midi/{user_id}/{song.title}.html"
        midi_path = "data/midi/"+file_name+".midi"
        midi_to_block(midi_path, "templates/" + midi_template)


        request.session["user_id"] = 1
        return redirect(f"/song/{song.id}", request)
