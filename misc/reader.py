#!/usr/bin/python3
'''
author: Tobias Weis
'''
import time
import RPi.GPIO as GPIO

input_pin = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(input_pin, GPIO.IN)

while True:
    if GPIO.input(input_pin) == 1:
        print("1")
    else:
        print("0")
    time.sleep(.1)

GPIO.cleanup()
