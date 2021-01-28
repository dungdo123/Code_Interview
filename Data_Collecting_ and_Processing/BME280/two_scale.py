
import matplotlib.pyplot as plt
import pandas as pd

# meat data
# pork_data = pd.read_csv("july_pork_temp.csv")
# dataFrame = pd.DataFrame(pork_data, columns=["pork", "temp"])
# pork = dataFrame.pork[0:5041]
# temp = dataFrame.temp[0:5041]

August_data = pd.read_csv("August_pork.csv")
dataFrame = pd.DataFrame(August_data, columns=["Temp", "Pork", "Fish", "Chicken"])

temp = dataFrame.Temp[1:5040]
Pork = dataFrame.Pork[1:5040]
Fish = dataFrame.Fish[1:5040]
Chicken = dataFrame.Chicken[1:5040]

# init figures
fig, ax1 = plt.subplots()
labels = ['24h', '48h', '72h', '96h', '120h', '144h', '168h']


# create label x-axis function
def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks([720, 1440, 2160, 2880, 3600, 4320, 5040])
    ax.set_xticklabels(labels)

# plot
plt.title("Air pressure - ambient temperature", fontsize='20')

# color = 'tab:red'
ax1.set_xlabel('time (h)', fontsize='20')
ax1.set_ylabel('Air-pressure hPa', fontsize='20')
ax1.set_xlim(0, 5041)
ax1.set_ylim(1005, 1040)
set_axis_style(ax1, labels)
ax1.plot(Pork, color='red', label='pork')
ax1.plot(Fish, color='blue', label='fish')
ax1.plot(Chicken, color='orange', label='chicken')
ax1.legend(loc='upper left', fontsize='18')
ax2 = ax1.twinx()
ax2.set_ylim(15,100)
ax2.set_ylabel('Temperature oC', fontsize='20')
ax2.plot(temp, color='orange', label='temp')

ax2.legend(fontsize='18')
plt.show()

