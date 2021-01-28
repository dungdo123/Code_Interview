import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# # # remove [] characters
# with open('temp_3/384h.txt', 'r') as infile, open('temp_3/384h_a.txt', 'w') as outfile:
#     data = infile.read()
#     data = data.replace("[", "")
#     data = data.replace("]", "")
#     outfile.write(data)

with open('temp_3/summary.txt', 'r') as infile, open('temp_3/summary_2.csv', 'w') as outfile:
    data = infile.read()
    outfile.write(data)
