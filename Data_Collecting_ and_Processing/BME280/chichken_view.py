import pandas as pd
import matplotlib.pyplot as plt

chicken_data = pd.read_csv('temp_3/summary_2.csv')
dataFrame = pd.DataFrame(chicken_data, columns=['Temp', 'Hum', 'Press'])
x = dataFrame.Temp[1:95760:19]
y = dataFrame.Hum
z = dataFrame.Press

df = pd.DataFrame(x)
df.to_csv('temp_new.csv', index=False)

# print(len(x))
plt.xlim(0, 100000)
plt.ylim(0, 100)
plt.plot(x)
plt.xlabel("Time (x2 minutes)")
plt.ylabel("Temp oC")
#
# plt.plot(y)
# plt.xlabel("Time (x2 minutes)")
# plt.ylabel("Humidity %")

# plt.plot(z)
# plt.xlabel("Time (x2 minutes) ")
# plt.ylabel("Pressure hPa")
#
plt.show()