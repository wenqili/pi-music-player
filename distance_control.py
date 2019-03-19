#!/usr/bin/python
import RPi.GPIO as GPIO
import time

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

try:
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
            dist = distance()
            print "Distance:",dist,"cm"
            time.sleep(0.1)

except KeyboardInterrupt:
      print("Stop by user")
      GPIO.cleanup()