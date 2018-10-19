import grovepi
import pandas as pd
import RPi.GPIO as GPIO
import subprocess
import time
from gpiozero import MCP3008
from sklearn.linear_model import LinearRegression
import random

# consts ------------------------------------------------------

STAGE_LENGTH = 100
GOAL_NUMBER = 10

TEST_DATA_CSV_FILE_NAME = "./test_data.csv"
FUNCTION_DATA_CSV_FILE_NAME = "./function_data.csv"
COLUMNS = ["angle", "goal_location"]

GREEN_LED_GPIO_OUTPUT = 14
ORANGE_LED_GPIO_OUTPUT = 15
RED_LED_GPIO_OUTPUT = 18

KEEPER_MOTOR_GPIO_OUTPUT1 = 20
KEEPER_MOTOR_GPIO_OUTPUT2 = 21

FIRING_MOTOR_GPIO_OUTPUT1 = 23 
FIRING_MOTOR_GPIO_OUTPUT2 = 24

CHANGE_FUNCTION_BUTTON_GPIO_INPUT = 17
BALL_FIRING_BUTTON_GPIO_INPUT = 27

# left to right
GOAL_BUTTON_1_GPIO_INPUT = 4
GOAL_BUTTON_2_GPIO_INPUT = 5
GOAL_BUTTON_3_GPIO_INPUT = 6
GOAL_BUTTON_4_GPIO_INPUT = 7
GOAL_BUTTON_5_GPIO_INPUT = 12
GOAL_BUTTON_6_GPIO_INPUT = 13
GOAL_BUTTON_7_GPIO_INPUT = 16
GOAL_BUTTON_8_GPIO_INPUT = 19
GOAL_BUTTON_9_GPIO_INPUT = 22
GOAL_BUTTON_10_GPIO_INPUT = 25 

ANGLE_SENSOR_MCP3008_INPUT = MCP3008(channel = 0, device = 0)

# -------------------------------------------------------------

# settings ----------------------------------------------------

GPIO.setmode(GPIO.BCM)

# output:
GPIO.setup(GREEN_LED_GPIO_OUTPUT, GPIO.OUT)    # Green LED
GPIO.setup(ORANGE_LED_GPIO_OUTPUT, GPIO.OUT)   # Orange LED
GPIO.setup(RED_LED_GPIO_OUTPUT, GPIO.OUT)      # Red LED
GPIO.setup(FIRING_MOTOR_GPIO_OUTPUT1, GPIO.OUT) # Firing motor1
GPIO.setup(FIRING_MOTOR_GPIO_OUTPUT2, GPIO.OUT) # Firing motor2
GPIO.setup(KEEPER_MOTOR_GPIO_OUTPUT1, GPIO.OUT) # Firing motor1
GPIO.setup(KEEPER_MOTOR_GPIO_OUTPUT2, GPIO.OUT) # Firing motor2

# input:
GPIO.setup(CHANGE_FUNCTION_BUTTON_GPIO_INPUT, GPIO.IN)  # Change Function Button
GPIO.setup(BALL_FIRING_BUTTON_GPIO_INPUT, GPIO.IN)  # Ball Firing Button
GPIO.setup(GOAL_BUTTON_1_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_2_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_3_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_4_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_5_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_6_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_7_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_8_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_9_GPIO_INPUT, GPIO.IN)  # Goal Button
GPIO.setup(GOAL_BUTTON_10_GPIO_INPUT, GPIO.IN)  # Goal Button

# -------------------------------------------------------------

# valiables ---------------------------------------------------

# training data utilization phase : 1
# training data collection phase : 0
function_condition = 0

# pushed   : 1
# unpushed : 0
change_function_button_condition = 0

# pushed   : 1
# unpushed : 0
ball_firing_button_condition = 0

# -------------------------------------------------------------

# getters -----------------------------------------------------

def get_change_function_button_condition():
  if GPIO.input(CHANGE_FUNCTION_BUTTON_GPIO_INPUT) == GPIO.HIGH:
    return 1
  else:
    return 0

def get_ball_firing_button_condition():
  if GPIO.input(BALL_FIRING_BUTTON_GPIO_INPUT) == GPIO.HIGH:
    return 1
  else:
    return 0

def get_goal_button_condition():
  if GPIO.input(GOAL_BUTTON_1_GPIO_INPUT) == GPIO.HIGH:
    return 1
  else:
    return 0

def get_angle():
  angle = ANGLE_SENSOR_MCP3008_INPUT.value
  return round(angle, 5)

def get_goal_location():
  start = time.time()
  for i in range(200000):
    if GPIO.input(GOAL_BUTTON_1_GPIO_INPUT) == GPIO.HIGH:
      return '1'
    if GPIO.input(GOAL_BUTTON_2_GPIO_INPUT) == GPIO.HIGH:
      return '2'
    if GPIO.input(GOAL_BUTTON_3_GPIO_INPUT) == GPIO.HIGH:
      return '3'
    if GPIO.input(GOAL_BUTTON_4_GPIO_INPUT) == GPIO.HIGH:
      return '4'
    if GPIO.input(GOAL_BUTTON_5_GPIO_INPUT) == GPIO.HIGH:
      return '5'
    if GPIO.input(GOAL_BUTTON_6_GPIO_INPUT) == GPIO.HIGH:
      return '6'
    if GPIO.input(GOAL_BUTTON_7_GPIO_INPUT) == GPIO.HIGH:
      return '7'
    if GPIO.input(GOAL_BUTTON_8_GPIO_INPUT) == GPIO.HIGH:
      return '8'
    if GPIO.input(GOAL_BUTTON_9_GPIO_INPUT) == GPIO.HIGH:
      return '9'
    if GPIO.input(GOAL_BUTTON_10_GPIO_INPUT) == GPIO.HIGH:
      return '10'
  elapsed_time = time.time() - start
  print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
  return 'None'

# -------------------------------------------------------------

# functions ---------------------------------------------------

def change_function_condition():
  global function_condition

  if function_condition == 1:
    function_condition = 0
  else:
    function_condition = 1

def led_default_light_up():
  global function_condition
  if function_condition == 1:
    GPIO.output(GREEN_LED_GPIO_OUTPUT,  True)
    GPIO.output(ORANGE_LED_GPIO_OUTPUT, False)
    
  elif function_condition == 0:
    GPIO.output(GREEN_LED_GPIO_OUTPUT,  False)
    GPIO.output(ORANGE_LED_GPIO_OUTPUT, True)

def fire_a_ball(move):
   if (move):
      # move downward
      GPIO.output(FIRING_MOTOR_GPIO_OUTPUT1, False)
      GPIO.output(FIRING_MOTOR_GPIO_OUTPUT2, True)
      time.sleep(0.4)

      GPIO.output(FIRING_MOTOR_GPIO_OUTPUT1, False)
      GPIO.output(FIRING_MOTOR_GPIO_OUTPUT2, False)

def move_a_keeper(moving_time):
  if moving_time > 0:
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT1, True)
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT2, False)
    time.sleep(moving_time)  
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT1, False)
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT2, False)
  elif moving_time < 0:
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT1, False)
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT2, True)
    time.sleep(-moving_time)  
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT1, False)
    GPIO.output(KEEPER_MOTOR_GPIO_OUTPUT2, False)

def write_function_csv_file():
  # Create dataset and including the first row by setting no header as input
  dataset = pd.read_csv(TEST_DATA_CSV_FILE_NAME)
  x = dataset[[COLUMNS[0]]].values
  y = dataset[COLUMNS[1]].values

  # Shape the goal location
  goal_length = STAGE_LENGTH / GOAL_NUMBER
  y = [goal_length * element + goal_length / 2.0 for element in y]

  # Learn the weight of linear model
  linear_regression = LinearRegression()
  linear_regression.fit(x, y)

  # set a coefficient and intercept
  data_frame = pd.DataFrame(
    [[linear_regression.coef_[0], linear_regression.intercept_]],
    columns=['coefficient', 'intercept']
  )
  data_frame.to_csv(FUNCTION_DATA_CSV_FILE_NAME, index=False, encoding='utf-8')

# -------------------------------------------------------------

# execution ---------------------------------------------------

# ------------------------------------------------------------------------------ TODO -----------------------------------------------------------------------------------
# move keeper to center
# move firing device to upward
# ------------------------------------------------------------------------------ TODO -----------------------------------------------------------------------------------

while True:
  try:
    change_function_button_condition = get_change_function_button_condition()
    ball_firing_button_condition = get_ball_firing_button_condition()
    print('ball_firing_button_condition: ' + str(ball_firing_button_condition))
    print('change_function_button_condition: ' + str(change_function_button_condition))

    if change_function_button_condition == 1:
      change_function_condition()

    led_default_light_up()

    # training data utilization phase
    if function_condition == 1:
      print("training data utilization phase")
      if ball_firing_button_condition == 1:
        print("ball firing !")

        # light up red LED
	GPIO.output(RED_LED_GPIO_OUTPUT, True)

	# get angle
        angle = get_angle()
	print('angle:' + str(angle))

	# fire a ball (operation moter)
        fire_a_ball()

	# ------------------------------------------------------------------------------ TODO -----------------------------------------------------------------------------------
	# move keeper (operation moter) : exactly
	# ------------------------------------------------------------------------------ TODO -----------------------------------------------------------------------------------

        # light down red LED
    	GPIO.output(RED_LED_GPIO_OUTPUT, False)

    # training data collection phase
    else:
      print("training data collection phase")

      if ball_firing_button_condition == 1:
        print("ball firing !")

        # light up red LED
    	GPIO.output(RED_LED_GPIO_OUTPUT, True)

	# get angle
	angle = get_angle()
	print('angle:' + str(angle))

        # fire a ball (operation moter)
        fire_a_ball(True)

	# ------------------------------------------------------------------------------ TODO -----------------------------------------------------------------------------------
	# move keeper (operation moter) : rondomly
	moving_time = random.uniform(1.25, -1.25)
        move_a_keeper(moving_time)

        # get goal_location
	goal_location = get_goal_location()
        print('goal_location: ' + goal_location)

        # write Test CSV file
	data = pd.DataFrame([[angle, goal_location]])
	data.to_csv(
          TEST_DATA_CSV_FILE_NAME, index=False, encoding='utf-8', mode='a', header=False
	)

        # calculate and write Function CSV file
	# write_function_csv_file()

        # fire a ball (operation moter) : return to	
        fire_a_ball(False)
	# move keeper (operation moter) : return to
        move_a_keeper(-moving_time)

        # light down red LED
    	GPIO.output(RED_LED_GPIO_OUTPUT, False)
	# ------------------------------------------------------------------------------ TODO -----------------------------------------------------------------------------------

    time.sleep(0.5)

  except IOError:
    print('Error !')

GPIO.cleanup()

# -------------------------------------------------------------
