import pandas as pd
import matplotlib.pyplot as plt


return_loss = pd.read_csv('return_loss.csv',index_col=0)
dataFrame = pd.DataFrame(return_loss, columns=['Freq', 'S11_simulation', 'S11_measured'])
x = dataFrame.Freq
y = dataFrame.S11_simulation
z = dataFrame.S11_measured
plt.plot(x, y, label = "Simulated", linewidth=5)
plt.plot(x, z, '--', label = "Measured", linewidth =5)
plt.xlabel("Frequency [GHz]", fontsize=25)
plt.ylabel("Reflection coef.[dB]", fontsize=25)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid('--')
plt.legend(loc='lower right', fontsize=25)
plt.show()