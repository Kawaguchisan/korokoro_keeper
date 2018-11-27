import pandas as pd
from consts import TEST_DATA_CSV_FILE_NAME

# getter -------------------
def get_angle():
    return "0"

def get_goal_location():
    return "0"
# --------------------------

# Set variable parameter ---
angle = get_angle()
goal_location = get_goal_location()
# --------------------------

# Create data frame
data = pd.DataFrame([[angle, goal_location]])

# Add training data
data.to_csv(TEST_DATA_CSV_FILE_NAME, index=False, encoding="utf-8", mode='a', header=False)
