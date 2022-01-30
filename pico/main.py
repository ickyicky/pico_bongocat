from oled import OLED_2inch23
from cat import FIRST, SECOND
import utime
from sys import stdin
import select


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


def clear(OLED):
    OLED.fill(0x0000)


def write_greet(OLED):
    OLED.text("UWU!", 64, 12, OLED.white)


def write_wpm(OLED, wpm):
    if wpm <= 10:
        write_greet(OLED)
    else:
        OLED.text(str(wpm), 64, 2, OLED.white)
        OLED.text("WPM", 64, 12, OLED.white)


def draw_first_cat(OLED):
    for x, y in FIRST:
        OLED.pixel(x, y, OLED.white)


def draw_second_cat(OLED):
    for x, y in SECOND:
        OLED.pixel(x, y, OLED.white)


def update_oled(OLED):
    WPM = 0
    while True:
        clear(OLED)
        write_wpm(OLED, WPM)
        draw_first_cat(OLED)
        OLED.show()

        speed = 0.4
        if WPM > 60:
            speed = 60 / WPM / 3

        utime.sleep(speed)
        clear(OLED)
        write_wpm(OLED, WPM)
        draw_second_cat(OLED)
        OLED.show()
        utime.sleep(speed)

        if theressome():
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


OLED = OLED_2inch23()
update_oled(OLED)
