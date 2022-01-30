from oled import OLED_2inch23
from cat import FIRST, SECOND, THIRD
import utime
from sys import stdin
import select


class CuteGreater:
    CUTE_WORDS = [
        "UWU!",
        "SUPER!",
        "CUTE!",
        "OK!",
        "HEY!",
        "WOW!",
        "AHAHA!",
        "WOA!",
    ]

    def __init__(self):
        self.word = 0
        self.i = 0
        self.last_displayed = False

    def next_word(self):
        self.word = (self.word + 1) % len(self.CUTE_WORDS)
        self.i = 0

    def next_phrase(self):
        word = self.CUTE_WORDS[self.word]

        if self.i < len(word):
            self.i += 1
            return word[: self.i]
        elif self.i == len(word) or self.i == len(word) + 2:
            self.i += 1
            return ""
        elif self.i == len(word) + 1:
            self.i += 1
            return word
        else:
            self.next_word()
            return word

    def write_to(self, OLED, wpm):
        OLED.fill(0x0000)
        if wpm == 0.0:
            phrase = self.next_phrase()
            OLED.text(phrase, 64, 12, OLED.white)
            for x, y in THIRD:
                OLED.pixel(x, y, OLED.white)
        else:
            OLED.text(str(wpm), 64, 2, OLED.white)
            OLED.text("WPM", 64, 12, OLED.white)
            if not self.last_displayed:
                self.last_displayed = True
                word = self.CUTE_WORDS[self.word]
                self.next_word()
                OLED.text(word, 64, 22, OLED.white)
                for x, y in FIRST:
                    OLED.pixel(x, y, OLED.white)
            else:
                self.last_displayed = False
                for x, y in SECOND:
                    OLED.pixel(x, y, OLED.white)
        OLED.show()


def theressome():
    if select.select(
        [
            stdin,
        ],
        [],
        [],
        0.0,
    )[0]:
        return True
    return False


def new_wpm():
    if not theressome():
        return
    WPM = 0
    for i in range(3):
        read = stdin.read(1)
        if read:
            try:
                WPM = int(read) + 10 * WPM
            except Exception:
                pass
        if not theressome():
            break
    return WPM


def update_oled(OLED):
    WPM = 0
    greeter = CuteGreater()

    while True:
        greeter.write_to(OLED, WPM)

        speed = 0.4
        if WPM > 60:
            speed = 60 / WPM / 8

        utime.sleep(speed)
        new_ = new_wpm()
        if new_ is not None:
            WPM = new_


OLED = OLED_2inch23()
update_oled(OLED)
