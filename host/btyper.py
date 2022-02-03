from evdev import InputDevice, categorize, KeyEvent, list_devices
import time
import os
from argparse import ArgumentParser
from threading import Thread


class WMPWatcher:
    """
    WMPWatcher watches WMP and overall typing on
    configured device.

    It stores information about current device:
        - if it is being typed on currently
        - if so, how fast
    """

    def __init__(self, word_len: int = 5):
        self._word_len = word_len
        self._is_typing = False
        self._wpm = 0.0
        self._sentence_start = None
        self._sentence_last = None
        self._sentence_len = 0

    @property
    def wpm(self) -> float:
        return self._wpm

    @property
    def is_typing(self) -> bool:
        return self._is_typing

    def watch_events(self, device: InputDevice) -> None:
        """
        This is a function supposed to be ran
        in thread, it updates sentence_len
        and sentence_last time.
        """
        for _event in device.read_loop():
            event = categorize(_event)

            if not isinstance(event, KeyEvent):
                continue

            if event.keystate != event.key_up:
                continue

            self._sentence_len += 1
            self._sentence_last = time.time()
            self._is_typing = True
            if self._sentence_start is None:
                self._sentence_start = self._sentence_last

    def update_state(self) -> None:
        """
        This is a function supposed to be ran
        in thread loop, it updates wmp and is_typing
        """
        if self._is_typing is False:
            return

        # If someone stuttered for more than 2 words
        # we consider he stopped typing
        curr_time = time.time()
        time_till_reset = 2 / (max(60, self._wpm)) * 60

        if curr_time - self._sentence_last >= time_till_reset:
            # stopped typing
            self._sentence_len = 0
            self._sentence_start = None
            self._sentence_last = None
            self._wpm = 0
            self._is_typing = False
        elif self._sentence_len > 1:
            # is still typing and can update WMP
            self._wpm = (
                self._sentence_len
                / self._word_len
                / (curr_time - self._sentence_start)
                * 60
            )

    def watch_state(self, how_often: int = 1) -> None:
        """
        This is a function supposed to be ran
        in thread, it creates state updating loop
        """
        while True:
            self.update_state()
            time.sleep(how_often)

    @classmethod
    def autodiscover(cls):
        """
        Auto discovers connected devices
        """
        devices = [InputDevice(d) for d in list_devices()]
        print("Now, start typing and type untill we say you not to!")
        time.sleep(2)
        print("You can stop typing now!")

        found_device = None
        for device in devices:
            for _ in range(5):
                _event = device.read_one()

                if not _event:
                    continue

                event = categorize(_event)
                if not isinstance(event, KeyEvent):
                    continue

                found_device = device

        assert found_device is not None, "Keyboard not detected! Try better!"
        return found_device


if __name__ == "__main__":
    from pico_updater import send_updates

    parser = ArgumentParser()
    parser.add_argument(
        "--device", "-d", required=False, help="Input device (keyboard)"
    )
    parser.add_argument("--port", "-p", required=False, help="TTY port for pico")
    args = parser.parse_args()
    device = None

    if args.device:
        device = InputDevice(args.device)
    else:
        device = WMPWatcher.autodiscover()

    port = args.port
    for p in os.listdir("/dev"):
        if p.startswith("ttyACM"):
            port = f"/dev/{p}"
            break

    watcher = WMPWatcher()
    watching_thread = Thread(target=watcher.watch_events, args=[device])
    watching_thread.start()
    updating_thread = Thread(target=watcher.watch_state)
    updating_thread.start()
    sending_thread = Thread(target=send_updates, args=[watcher, port])
    sending_thread.start()
    watching_thread.join()
    updating_thread.join()
    sending_thread.join()
