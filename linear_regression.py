# Import Libraries
from consts import STAGE_LENGTH
from consts import GOAL_NUMBER
from consts import TEST_DATA_CSV_FILE_NAME
from consts import FUNCTION_DATA_CSV_FILE_NAME
from consts import COLUMNS
from sklearn.linear_model import LinearRegression
import pandas as pd

# Create Dataset and including the first row by setting no header as input
dataset = pd.read_csv(TEST_DATA_CSV_FILE_NAME)
x = dataset[[COLUMNS[0]]].values
y = dataset[COLUMNS[1]].values

# Shape the goal location
goal_length = STAGE_LENGTH / GOAL_NUMBER
y = [goal_length * element + goal_length / 2.0 for element in y]

# Learn the weight of linear model
lr = LinearRegression()
lr.fit(x, y)

# Set a coefficient and intercept
df = pd.DataFrame([[lr.coef_[0], lr.intercept_]], columns=["coefficient", "intercept"])
df.to_csv(FUNCTION_DATA_CSV_FILE_NAME, index=False, encoding="utf-8")
