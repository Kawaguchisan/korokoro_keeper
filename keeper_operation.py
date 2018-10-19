import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

while True:
  GPIO.output(20, True)
  GPIO.output(21, False)
  time.sleep(5)

  GPIO.output(20, False)
  GPIO.output(21, False)
  time.sleep(0.5)

  GPIO.output(20, False)
  GPIO.output(21, True)
  time.sleep(5)

GPIO.cleanup()

