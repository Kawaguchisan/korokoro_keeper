from gpiozero import MCP3008
from time import sleep

tmp = MCP3008(channel=0, device=0)

while True:
  angle = tmp.value
  print(round(angle, 5))
  sleep(1)

