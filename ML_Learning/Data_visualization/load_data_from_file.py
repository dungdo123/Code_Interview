import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('example.txt','r') as csvfile:
    plots = csv.reader(csvfile)
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

plt.plot(x,y,label = 'load from file')
plt.xlabel('x')
plt.ylabel('y')
plt.title('csv data')
plt.legend()
plt.show()