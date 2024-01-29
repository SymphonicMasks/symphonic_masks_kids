import os.path
from pathlib import Path

from django.http import HttpResponse
from pretty_midi import PrettyMIDI

from bs4 import BeautifulSoup
from .utlilts import handle_uploaded_file, audio_to_midi, handle_user_recording
from .forms import UploadFileForm
from django.db import IntegrityError
# from django.conf import settings
from kids_app import settings
from django.shortcuts import render, redirect, reverse
from .models import Song
from infrastructure import basic_pitcher, music21_renderer, MusicSubmission


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
        song = Song.objects.get(pk=1)

        user_id = 1
        midi_template = f"user_midi/{user_id}/{song.title}.html"
        midi_path = "data/midi/" + file_name + ".midi"
        # midi_to_block(midi_path, "templates/" + midi_template)
        music21_renderer.generate_html_block(midi_data=midi_data)
        request.session["user_id"] = 1
        return redirect(f"/song/{song.id}", request)


def record(request):
    if request.method == "GET":
        form = UploadFileForm()
        context = {"form": form}
        if request.session.has_key("errors"):
            context["errors"] = request.session["errors"]
        return render(request, "recorder.html", context)

    else:
        file = request.FILES["file"]
        file_url = handle_uploaded_file(file)
        file_name = file.name.split(".")[0]
        media = settings.MEDIA_ROOT
        midi_data = basic_pitcher(media + "/" + file.name, "data/midi/" + file_name + ".midi")

        song = Song.objects.get(pk=1)
        user_id = 1
        original_stream = music21_renderer.read_xml("data/xml/k.xml")
        user_notes, tempo = music21_renderer.get_notes_from_midi(midi_data)
        viz_path = media + f"/submissions/{user_id}/{song.id}.xml"

        submission = MusicSubmission(original_stream, user_notes, tempo, viz_path)
        submission.make_viz(make_svg=True)

        return redirect(reverse("songs:show_result", kwargs={"score_path": viz_path}))


def upload_recording(request):
    if request.method == "POST":
        file = request.FILES["file"]
        session_id = request.session.session_key
        handle_user_recording(file, session_id)

        return HttpResponse(content="ok", status=200)


def show_result(request):
    if request.method == "GET":
        redirect("/", request)
    else:
        file = request.FILES["file"]
        file_url = handle_uploaded_file(file)
        file_name = file_url.split("/")[-1]
        media = settings.MEDIA_ROOT
        midi_data = basic_pitcher(media + "/" + file_name, "data/midi/" + file_name + ".midi")

        song = Song.objects.get(pk=1)
        user_id = 1
        original_stream = music21_renderer.read_xml("data/xml/k.xml")
        user_notes, tempo = music21_renderer.get_notes_from_midi(midi_data)
        if tempo == 0:
            request.session["errors"] = "Что-то пошло не так, может ты играл слишком тихо?"
            return redirect("/", request)

        if len(user_notes) < 10:
            request.session["errors"] = "Ты так мало играл(("
            return redirect("/", request)

        viz_path = media + f"/submissions/{user_id}/{song.id}.xml"
        submission = MusicSubmission(original_stream, user_notes, tempo, viz_path)
        submission.make_viz(make_svg=False)

        return render(request, "results.html", {"score_path": viz_path})
