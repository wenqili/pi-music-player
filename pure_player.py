#!/user/bin/python

import os
import subprocess
import glob
import time
import RPi.GPIO as GPIO

os.chdir('/home/pi/music_player/')
file = glob.glob('*mp3')
pointer = 0

# initial status
status = 1
volume = 15

# two steps means max Volume: 6.00dB
minDist = volume
maxDist = volume + 40
dist = 0


def distance():
    # set Trigger to HIGH
    GPIO.output(PIN_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(PIN_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(PIN_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2

    return distance


def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


if __name__ == '__main__':
    try:

        # set up distance sensor
        GPIO.setmode(GPIO.BOARD)

        PIN_TRIGGER = 7
        PIN_ECHO = 11

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        print "Waiting for sensor to settle"

        time.sleep(2)

        print "Calculating distance"

        while True:
            # calculate distance
            rawDist = distance()
            proDist = map(rawDist, 0, 120, minDist, maxDist)

            # corp the extra
            if (proDist > maxDist):
                proDist = maxDist
            elif (proDist < minDist):
                proDist = minDist1

            dist = int(proDist)
            time.sleep(0.1)

            # initial status
            if(status == 1):
                player = subprocess.Popen(
                    ["omxplayer", file[pointer]], stdin=subprocess.PIPE)
                fi = player.poll()
                status = 0
                volume = 15

            # volumn control
            if (dist >= 0 and dist <= maxDist and fi != 0):
                vol = dist

                # if get closer
                if (vol > volume):
                    for i in range(1, vol - volume):
                        # volume level up in omxplayer
                        player.stdin.write("-")
                        # volume level up
                        volume = volume + 1
                        print volume
                        time.sleep(0.1)

                # if get away
                elif (vol < volume):
                    for i in range(1, volume - vol):
                        # volume level down in omxplayer
                        player.stdin.write("+")
                        # volume level down
                        volume = volume - 1
                        print volume
                        time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopped by user")
        GPIO.cleanup()
