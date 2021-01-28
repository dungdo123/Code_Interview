import pandas as pd
import matplotlib.pyplot as plt

pork_data = pd.read_csv("pork_start.csv")
dataFrame = pd.DataFrame(pork_data, columns=["Time", "ColorTemp", "Lux", "Red", "Green", "Blue", "Clear"])
print(dataFrame)
Time = dataFrame.Time
ColorTemp = dataFrame.ColorTemp
Lux = dataFrame.Lux
R1 = dataFrame.Red
G1 = dataFrame.Green
B1 = dataFrame.Blue
C1 = dataFrame.Clear
print(R1[10])
fig, ax1 = plt.subplots(2, 2)

# draw R, G, B
ax1[0,0].set_xlabel('number of measurements', fontsize='20')
ax1[0,0].set_ylabel('RGB color', fontsize='20')
ax1[0,0].set_xlim(0, 7200)
ax1[0,0].set_ylim(2300, 4100)
ax1[0,0].plot(R1, color='red', label="Red")
ax1[0,0].plot(G1, color='green', label='Green')
ax1[0,0].plot(B1, color='blue', label='Blue')
ax1[0,0].legend()

# Draw Colortemp
ax1[0,1].set_xlabel('number of measurements', fontsize='20')
ax1[0,1].set_ylabel('TempColor', fontsize='20')
ax1[0,1].set_xlim(0, 7200)
ax1[0,1].set_ylim(5000, 7000)
ax1[0,1].plot(ColorTemp, label='color temperature')
ax1[0,1].legend()

# Draw Lux
ax1[1,0].set_xlabel('number of measurements', fontsize='20')
ax1[1,0].set_ylabel('Lux', fontsize='20')
ax1[1,0].set_xlim(0, 7200)
ax1[1,0].set_ylim(1000,2000)
ax1[1,0].plot(Lux, label='Lux indicator')
ax1[1,0].legend()

# Draw Clear
ax1[1,1].set_xlabel('number of measurements', fontsize='20')
ax1[1,1].set_ylabel('Clear', fontsize='20')
ax1[1,1].set_xlim(0, 7200)
ax1[1,1].set_ylim(9000, 12000)
ax1[1,1].plot(C1, label='clear indicator')
ax1[1,1].legend()
plt.show()
