from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1, projection='3d')

x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array([5,6,7,8,2,5,6,3,7,2])
z = np.array([[1,2,6,3,2,7,3,3,7,2],[1,2,6,3,2,7,3,3,7,2]])
ax1.plot_wireframe(x,y,z)

ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_zlabel('z axis')

plt.show()

