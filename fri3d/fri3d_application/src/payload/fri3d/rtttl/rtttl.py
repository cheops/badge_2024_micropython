import logging
import math
import time

from fri3d.badge.buzzer import buzzer

logger = logging.Logger('rtttl')


class RTTTL:
    # You can find a description of RTTTL here: https://en.wikipedia.org/wiki/Ring_Tone_Text_Transfer_Language
    _NOTES = [
        440.0,  # A
        493.9,  # B or H
        261.6,  # C
        293.7,  # D
        329.6,  # E
        349.2,  # F
        392.0,  # G
        0.0,  # pad

        466.2,  # A#
        0.0,
        277.2,  # C#
        311.1,  # D#
        0.0,
        370.0,  # F#
        415.3,  # G#
        0.0,
    ]

    def __init__(self, tune: str):
        tune_pieces = tune.split(':')
        if len(tune_pieces) != 3:
            raise ValueError('Tune should contain exactly 2 colons')

        self.name = tune_pieces[0]

        logger.debug(f"Parsing RTTTL {self.name}")
        self.tune = tune_pieces[2]
        self.tune_idx = 0
        self._parse_defaults(tune_pieces[1])

    def _parse_defaults(self, defaults: str):
        # Example: d=4,o=5,b=140
        value = 0

        for item in defaults.split(','):
            setting = item.split('=')

            key = setting[0].strip()
            value = int(setting[1].strip())

            if key == 'o':
                self.default_octave = value
            elif key == 'd':
                self.default_duration = value
            elif key == 'b':
                self.bpm = value

        # 240000 = 60 sec/min * 4 beats/whole-note * 1000 msec/sec
        self.msec_per_whole_note = 240000.0 / self.bpm

    def _next_char(self):
        if self.tune_idx < len(self.tune):
            char = self.tune[self.tune_idx]
            self.tune_idx += 1
            if char == ',':
                char = ' '
            return char
        return '|'

    def _notes(self):
        """Generator which generates notes. Each note is a tuple where the
           first element is the frequency (in Hz) and the second element is
           the duration (in milliseconds).
        """
        while True:
            # Skip blank characters and commas
            char = self._next_char()
            while char == ' ':
                char = self._next_char()

            # Parse duration, if present. A duration of 1 means a whole note.
            # A duration of 8 means 1/8 note.
            duration = 0
            while char.isdigit():
                duration *= 10
                duration += ord(char) - ord('0')
                char = self._next_char()
            if duration == 0:
                duration = self.default_duration

            if char == '|':  # marker for end of tune
                return

            note = char.lower()
            if 'a' <= note <= 'g':
                note_idx = ord(note) - ord('a')
            elif note == 'h':
                note_idx = 1  # H is equivalent to B
            else:
                note_idx = 7  # pause
            char = self._next_char()

            # Check for sharp note
            if char == '#':
                note_idx += 8
                char = self._next_char()

            # Check for duration modifier before octave
            # The spec has the dot after the octave, but some places do it
            # the other way around.
            duration_multiplier = 1.0
            if char == '.':
                duration_multiplier = 1.5
                char = self._next_char()

            # Check for octave
            if '4' <= char <= '7':
                octave = ord(char) - ord('0')
                char = self._next_char()
            else:
                octave = self.default_octave

            # Check for duration modifier after octave
            if char == '.':
                duration_multiplier = 1.5
                char = self._next_char()

            freq = self._NOTES[note_idx] * (1 << (octave - 4))
            msec = (self.msec_per_whole_note / duration) * duration_multiplier

            yield freq, msec

    @staticmethod
    def _play_tone(freq: float, msec: float, duty: int):
        logger.debug('Note freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
        if freq > 0:
            buzzer.freq(int(freq))
            buzzer.duty_u16(duty)

        time.sleep_ms(int(msec * 0.9))
        buzzer.duty_u16(0)
        time.sleep_ms(int(msec * 0.1))

    def play(self, volume: int = 100):
        print(f"Playing '{self.name}'")
        if volume <= 0:
            duty = 0
        else:
            if volume > 100:
                volume = 100

            # This calculation is based on absolutely no scientific data at all and was chosen because it sounds ok.
            # Maximum volume is at 50% duty cycle (which _is_ a fact)
            # Lower volumes are calculated using an exponential scale as the amount of volume change is bigger at the
            # very low duty cycles
            # The absolute minimum (again, very unscientifically tested) is 4 when using PWM.duty_u16

            # By changing the divider you can move the calculation on the exponential scale. Higher values for the
            # divider favor bigger steps at the low end of the duty cycle.
            divider = 10
            duty = int(
                (
                        (math.exp(volume / divider) - math.exp(0.1)) /
                        (math.exp(10) - math.exp(0.1)) *
                        (32768 - 4)
                ) + 4
            )

        try:
            for freq, msec in self._notes():
                self._play_tone(freq, msec, duty)
        finally:
            self._play_tone(0, 0, 0)
