from basic_pitch.inference import predict
import pretty_midi
from IPython.display import Audio
import csv


def midi_to_notes(midi_data):
    notes = []
    beats_per_second = midi_data.estimate_tempo() / 60
    avg_note_time = 1 / beats_per_second
    print(avg_note_time)
    for instrument in midi_data.instruments:
        for i, note in enumerate(instrument.notes):
            note_time = note.end - note.start
            if note_time / avg_note_time < 0.7 \
                    and i > 0:
                print(note_time / avg_note_time)

                print(note.pitch)
                if note.pitch == instrument.notes[i - 1].pitch:
                    instrument.notes[i - 1].end = note.end
                    continue

            notes.append(note)

    return notes


def notes_to_csv(notes, output):
    f = open(output, "a+")
    writer = csv.writer(f)
    row = []
    for n in notes:
        row.append(pretty_midi.note_number_to_name(n.pitch))

    writer.writerow(row)
    f.close()


model_output, midi_data, note_events = predict("data/forest.m4a")
notes = midi_to_notes(midi_data)
midi_data.write("forest.midi")
notes_to_csv(notes, "forest.csv")
midi = pretty_midi.PrettyMIDI()
