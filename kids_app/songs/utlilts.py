import os.path
import pathlib

from basic_pitch.inference import predict
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def handle_uploaded_file(file):
    fss = FileSystemStorage()
    file = fss.save(file.name, file)
    file_url = fss.url(file)

    return file_url


def handle_user_recording(file, session_id: str) -> str:
    fss = FileSystemStorage()
    media_path = settings.MEDIA_ROOT
    # user_path = f"{media_path}/submissions/{session_id}/"
    # pathlib.Path(user_path).mkdir(exist_ok=True)

    file = fss.save(f"submissions/{session_id}/audio.wav", file)
    file_url = fss.url(file)

    return file_url


def audio_to_midi(audio, output_path):
    model_output, midi_data, note_events = predict(audio)
    midi_data.write(output_path)

    return output_path
