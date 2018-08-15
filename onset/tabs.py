import json
import os.path

import librosa

FRETS = [0.2, 0.4, 0.6, 0.8, 1]
TABS_DIR = 'tabs'


def fret(strength):
    for i, value in enumerate(FRETS):
        if strength <= value:
            return i


class TabsBuilder:
    def __init__(self, source_file):
        audio_data, sampling_rate = librosa.load(source_file)
        harmonic = librosa.effects.harmonic(audio_data)

        self.onset_envelope = librosa.onset.onset_strength(harmonic, sampling_rate)
        onsets = librosa.onset.onset_detect(onset_envelope=self.onset_envelope)
        self.onset_times = librosa.frames_to_time(onsets, sr=sampling_rate)

    def generate_tabs(self):
        for time in self.onset_times:
            frame = librosa.time_to_frames([time])[0]
            strength = self.onset_envelope[frame]
            yield dict(time=time, strength=strength)


def load_tabs(source_file):
    base_name = os.path.basename(source_file)
    tabs_file_path = os.path.join(TABS_DIR, f'{base_name}.json')

    if os.path.exists(tabs_file_path):
        with open(tabs_file_path) as f:
            return json.load(f)

    else:
        if not os.path.exists(TABS_DIR):
            os.mkdir(TABS_DIR)

        tabs = list(TabsBuilder(source_file).generate_tabs())
        with open(tabs_file_path, 'w') as f:
            json.dump(tabs, f)
        return tabs
