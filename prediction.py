# Import Libraries
from consts import STAGE_LENGTH
from consts import GOAL_NUMBER
from consts import FUNCTION_DATA_CSV_FILE_NAME
import pandas as pd

# getter -------------------
def get_angle():
    return 3
# --------------------------

# Set variable parameter ---
angle = get_angle()
# --------------------------

# Read function data
dataset = pd.read_csv(FUNCTION_DATA_CSV_FILE_NAME)
coefficient = dataset['coefficient'].values[0]
intercept = dataset['intercept'].values[0]

# Predict goal_length
goal_length = angle * coefficient + intercept

print(goal_length)


