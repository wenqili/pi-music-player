#!/usr/bin/env python3

import time
import aiy.voice.tts
from aiy.board import Board, Led
import subprocess
import os

FILE_PATH = '/home/pi/music_player/track.mp3'


class MediaPlayer():
    def __init__(self):
        self.url = None
        self.process = None

    def play(self, url):
        self.url = url
        self.process = subprocess.Popen(
            ['omxplayer', '-o', 'alsa', self.url], stdin=subprocess.PIPE)
        self.process.stdin.write(b'1')
        self.process.stdin.flush()

    def stop(self):
        self.process.stdin.write(b'q')
        self.process.stdin.flush()

    def volumeUp(self):
        self.process.stdin.write(b'+')
        self.process.stdin.flush()

    def volumeDown(self):
        self.process.stdin.write(b'-')
        self.process.stdin.flush()


if __name__ == '__main__':
    try:
        print("waiting for guesture")
        counter = 0
        startTime = time.time()
        releaseTime = time.time()
        timeGap = 0
        toggle = False
        player = MediaPlayer()

        with Board() as board:
            while True:
                board.button.wait_for_press()
                board.led.state = Led.ON
                startTime = time.time()

                board.button.wait_for_release()
                board.led.state = Led.OFF
                counter = counter + 1
                releaseTime = time.time()
                timeGap = releaseTime - startTime
                print("button pressed, and now counter = ", counter, timeGap)

                if (timeGap > 2 and toggle == False and timeGap <= 6):
                    player.play(FILE_PATH)
                    toggle = True
                    counter = 0
                    print("palyer start")
                elif (timeGap > 6):
                    aiy.voice.tts.say("Good bye")
                    subprocess.call('sudo shutdown now', shell=True)

                elif (timeGap > 2 and toggle == True):
                    player.stop()
                    toggle = False
                    counter = 0
                    print("Player stopped")

                if (toggle == False and counter > 1):
                    aiy.voice.tts.say(
                        "long press the button to play the track!")

                elif (toggle == True and counter <= 8 and counter != 0):
                    player.volumeDown()
                    print("Volume Down")

                elif (toggle == True and counter > 8 and counter <= 16):
                    player.volumeUp()
                    print("Volume Up")

                elif (toggle == True and counter > 16):
                    counter = 0
                    print("reset counter")

    except KeyboardInterrupt:
        player.stop()
        print("stopped")
