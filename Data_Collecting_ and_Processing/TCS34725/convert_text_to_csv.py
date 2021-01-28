# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# remove not necessary characters
with open('data/pork_start.txt', 'r') as infile, open('output/pork_start.csv', 'w') as outfile:
    data = infile.read()
    data = data.replace("b", "")
    data = data.replace("'", "")
    data = data.replace('"', "")
    data = data.replace("'", "")

    outfile.write(data)

