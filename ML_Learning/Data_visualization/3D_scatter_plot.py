from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

# x = np.array([1,2,3,4,5,6,7,8,9,10])
# y = np.array([5,6,7,8,2,5,6,3,7,2])
# z = np.array([[1,2,6,3,2,7,3,3,7,2],[1,2,6,3,2,7,3,3,7,2]])
#
# x2 = np.array([-1,-2,-3,-4,-5,-6,-7,-8,-9,-10])
# y2 = np.array([-5,-6,-7,-8,-2,-5,-6,-3,-7,-2])
# z2 = np.array([[1,2,6,3,2,7,3,3,7,2],[1,2,6,3,2,7,3,3,7,2]])
x = [1,2,3,4,5,6,7,8,9,10]
y = [5,6,7,8,2,5,6,3,7,2]
z = [1,2,6,3,2,7,3,3,7,2]

x2 = [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
y2 = [-5,-6,-7,-8,-2,-5,-6,-3,-7,-2]
z2 = [1,2,6,3,2,7,3,3,7,2]
ax1.scatter(x, y, z, c='g', marker='o')
ax1.scatter(x2, y2, z2, c ='r', marker='o')

ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_zlabel('z axis')

plt.show()