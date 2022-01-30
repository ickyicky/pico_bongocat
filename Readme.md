# BONGO CAT!

[![](https://github.com/ickyicky/pico_bongocat/blob/main/data/result.gif?raw=true)](https://github.com/ickyicky/pico_bongocat)

We all love watching our WPM and bongo cat, so this project enables us to enjoy both at the same time! Result of running code fromthis repo is bongo cat playing on your Raspberry Pi Pico OLED screen, showing you your WPM (if you are typing). Also, the faster you type, the faster bongo cat hits his bongos!

## Requirements

Bongo Cat was written for rpi pico with 2.23 inch SPI connected oled display. If you use different OLED simply alter `pico/oled.py` implementation.

Host part of code (basically keylogger logging wpm) was written purerly for Linux host. Watching input events requires user membership of **input** group, accessing tty of rpico requires membership of **uucp** group.

## Usage

### RPI Pico

Simply copy all `*.py` files to `/pyboard/` directory on your raspberry pi pico. Running code requires micropython support installed.

### Host

On host run `btyper.py` from `host` folder. It should autodiscover keyboard input (by listening to events and then fildering input devices with *KeyInput* ones) and pico tty, but if it has troubles with it simply identify input device yourself and use arguments: **--device** and **--port**. You can access help by running **python btyper.py --help**.
