import os.path
from pretty_midi import PrettyMIDI

from bs4 import BeautifulSoup
from .utlilts import handle_uploaded_file, audio_to_midi
from .forms import UploadFileForm
from django.db import IntegrityError
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from .models import Song
from infrastructure import basic_pitcher, music21_renderer


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
        del request.session['user_id']

    midi_path = song.midi_path
    midi_template = f"songs/{song.title}.html"
    # midi_to_block(midi_path, "templates/" + midi_template)

    context["song_midi"] = midi_template

    return render(request, "main.html", context)


def upload_audio(request):
    if request.method == "GET":
        form = UploadFileForm()
        return render(request, "upload.html", {"form": form})

    else:
        file = request.FILES["file"]
        file_url = handle_uploaded_file(file)
        file_name = file.name.split(".")[0]
        media = settings.MEDIA_ROOT
        midi_data = basic_pitcher(media + "/" + file.name, "data/midi/" + file_name + ".midi")

        if "song" not in request.POST.keys():
            try:
                song = Song(title=file_name)
                song.save()
            except IntegrityError as e:
                song = Song.objects.get(title=file_name)

            return redirect(f"/song/{song.id}", request)

        song_id = request.POST["song"]
        song = Song.objects.get(pk=song_id)

        user_id = 1
        midi_template = f"user_midi/{user_id}/{song.title}.html"
        midi_path = "data/midi/" + file_name + ".midi"
        # midi_to_block(midi_path, "templates/" + midi_template)
        music21_renderer.generate_html_block(midi_data=midi_data)
        request.session["user_id"] = 1
        return redirect(f"/song/{song.id}", request)
