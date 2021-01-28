import pandas as pd
import matplotlib.pyplot as plt

# pork_data = pd.read_csv("pork.csv", index_col=0)
# dataFrame = pd.DataFrame(pork_data, columns=["number", "pork", "chicken" ,"fish"])
pork_data = pd.read_csv("july_pork_temp.csv")
dataFrame = pd.DataFrame(pork_data, columns=["pork", "temp"])

# chicken = dataFrame.chicken[1:3600]
pork = dataFrame.pork[1:3600]
# fish = dataFrame.fish[1:3600]
# temp = dataFrame.Temp[1:3600]
fig, ax = plt.subplots()
labels = ['12h', '24h', '36h', '48h', '60h', '72h', '84h', '96h', '108h', '120h']
def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks([360, 720, 1080, 1440, 1880, 2160, 2520, 2880, 3240, 3600])
    ax.set_xticklabels(labels)

# press
plt.title('Air Pressure inside Food Package during 5 days', fontsize='20')
plt.xlim(0, 3600)
plt.ylim(1000, 1040)
set_axis_style(ax, labels)
# plt.plot(chicken, color='green', label="chicken")
plt.plot(pork, color='blue', label="pork")
# plt.plot(fish, color='red', label="fish")


# plt.plot(temp, color="red", label="temp")
plt.xlabel("Time", fontsize='20')
plt.ylabel("Air pressure hPa", fontsize='20')
plt.legend()
plt.show()

