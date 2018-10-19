import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

while True:
  # move downward
  GPIO.output(23, True)
  GPIO.output(24, False)
  time.sleep(0.3)

  # stop
  GPIO.output(23, False)
  GPIO.output(24, False)
  time.sleep(0.3)

  # move upward
  GPIO.output(23, False)
  GPIO.output(24, True)
  time.sleep(0.3)

  break 
GPIO.cleanup()

