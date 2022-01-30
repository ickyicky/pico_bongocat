import serial
import time
from typing import Any


def serial_for(port: str) -> "serial.Serial":
    return serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
    )


def send_updates(watcher: Any, port: str, how_often=1.0):
    serial = serial_for(port)
    last_wpm = -1

    while True:
        wpm = watcher.wpm
        if wpm != last_wpm:
            last_wpm = int(wpm)
            message = str(last_wpm)
            serial.write(message.encode())
            print(f"SENDING: {message}")
        time.sleep(how_often)
