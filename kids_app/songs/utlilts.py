import os.path
from basic_pitch.inference import predict


from bs4 import BeautifulSoup

from django.core.files.storage import FileSystemStorage
#
#
# def midi_to_block(midi_path: str, target_path):
#     pm = PrettyMIDI(midi_path)
#     pm.estimate_beat_start()
#     plotter = Plotter()
#     pm.get_piano_roll()
#     plotter.save(pm, target_path)
#
#     with open(target_path, "r") as f:
#         html_doc = f
#         soup = BeautifulSoup(html_doc, "html.parser")
#         soup.find('head').decompose()
#         soup.html.unwrap()
#         soup.body.unwrap()
#
#     with open(target_path, "w") as f:
#         f.write(
#             str(soup).replace("<!DOCTYPE html>", "")
#         )
#
#     return target_path


def handle_uploaded_file(file):
    fss = FileSystemStorage()
    file = fss.save(file.name, file)
    file_url = fss.url(file)

    return file_url


def audio_to_midi(audio, output_path):
    model_output, midi_data, note_events = predict(audio)
    midi_data.write(output_path)

    return output_path
