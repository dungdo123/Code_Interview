import pandas as pd
from collections import deque
import random
import numpy as np
from sklearn import preprocessing

# Creating the time-series index
ind = pd.date_range('01/01/2000', periods=6, freq='W')

# Creating the dataframe
df = pd.DataFrame({"A":[14, 4, 5, 4, 1, 55],
                   "B":[5, 2, 54, 3, 2, 32],
                   "C":[20, 20, 7, 21, 8, 5],
                   "D":[14, 3, 6, 2, 6, 4]}, index = ind)
#print(df)
for col in df.columns:
    if col == "A":
        df[col] = df[col].pct_change()
        #df.dropna(inplace=True)
        df[col] = preprocessing.scale(df[col].values)
for col in df.columns:
    if col == "B":
        df[col] = preprocessing.scale(df[col].values)
print(df)
