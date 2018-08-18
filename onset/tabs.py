import json
import os.path

import librosa

import constants


def fret(strength):
    for i, threshold in enumerate(constants.FRETS):
        if strength <= threshold:
            return i


class TabBuilder:
    def __init__(self, source_file):
        audio_data, sampling_rate = librosa.load(source_file)

        self.onset_envelope = librosa.onset.onset_strength(audio_data, sampling_rate)
        onsets = librosa.onset.onset_detect(onset_envelope=self.onset_envelope)
        self.onset_times = librosa.frames_to_time(onsets, sr=sampling_rate)

    def generate_tabs(self):
        for time in self.onset_times:
            frame = librosa.time_to_frames([time])[0]
            strength = self.onset_envelope[frame]
            yield dict(time=time, strength=strength)


def load_file(source_file):
    base_name = os.path.basename(source_file)
    tab_file_path = os.path.join(constants.TABS_DIR, f'{base_name}.json')

    if os.path.exists(tab_file_path):
        with open(tab_file_path) as f:
            return json.load(f)

    else:
        if not os.path.exists(constants.TABS_DIR):
            os.mkdir(constants.TABS_DIR)

        tab = list(TabBuilder(source_file).generate_tabs())
        with open(tab_file_path, 'w') as f:
            json.dump(tab, f)
        return tab


def load_notes(source_file):
    notes = load_file(source_file)
    result = [annotate(notes[0])]

    for index, note in enumerate(notes[1:]):
        if not within_time_window(note, result[-1]['time']):
            result.append(annotate(note, index))

    return result


def annotate(note, index=0):
    return {**note, 'hit': False, 'index': index}


def within_time_window(note, time, window=constants.NOTE_WINDOW):
    return abs(note['time'] - time) < window
