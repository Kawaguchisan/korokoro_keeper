import pandas as pd
from consts import TEST_DATA_CSV_FILE_NAME
from consts import COLUMNS

# Create data frame
df = pd.DataFrame([], columns=COLUMNS)

# Reset training data
df.to_csv(TEST_DATA_CSV_FILE_NAME, index=False, encoding="utf-8")
