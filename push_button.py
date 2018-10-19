import grovepi
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

while True:
  try:
    if GPIO.input(4) == GPIO.HIGH:
      print('1')
    else:
      print('0')
    time.sleep(0.5)

  except IOError:
    print('Error !')

