import sys
from time import time

from playsound import playsound
import librosa
import pyxel


AUDIO_FILE = sys.argv[1]


class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.audio_data, self.sampling_rate = librosa.load(AUDIO_FILE)

        self.harmonic = librosa.effects.harmonic(self.audio_data)

        self.onset_envelope = librosa.onset.onset_strength(self.harmonic, self.sampling_rate)
        self.onset_envelope_times = librosa.samples_to_frames(self.onset_envelope)

        self.onsets = librosa.onset.onset_detect(onset_envelope=self.onset_envelope)
        self.onset_times = librosa.frames_to_time(self.onsets, sr=self.sampling_rate)

        self.current_onset_envelope = 0
        self.current_onset_strength = 0
        self.current_onset = 0
        self.start_time = None
        self.playing = False


    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.playing:
            self.playing = True
            self.start_time = time()
            playsound(AUDIO_FILE, block=False)
        else:
            if (time() - self.start_time) >= self.onset_times[self.current_onset]:
                self.current_onset = min(self.current_onset + 1, len(self.onset_times) - 1)

                frame = librosa.time_to_frames((time() - self.start_time,))[0]
                if frame < len(self.onset_envelope):
                    self.current_onset_strength = self.onset_envelope[frame]

    def draw(self):
        pyxel.cls(0)

        pyxel.text(10, 10, f'{pyxel.frame_count}', 7)

        pyxel.text(30, 10, f'{self.current_onset} {self.onsets[self.current_onset]}', 7)

        strength = int(100 * self.current_onset_strength)
        pyxel.text(10, 30, f'{strength}', 8)
        pyxel.rect(30, 30, 30 + strength, 40, 8)


if __name__ == '__main__':
    Game().run()
