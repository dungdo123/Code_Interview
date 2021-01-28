import matplotlib.pyplot as plt

days = [1,2,3,4,5]

sleeping =[6,5,7,8,7]
working =[6,7,8,6,7]
eating =[1,2,1,2,1]
playing =[11,10,8,8,9]

plt.plot([],[],color='m', label='Sleeping', linewidth=5)
plt.plot([],[],color='c', label='Eating', linewidth=5)
plt.plot([],[],color='r', label='Working', linewidth=5)
plt.plot([],[],color='k', label='Playing', linewidth=5)

plt.stackplot(days, sleeping,eating,working,playing, colors=['m','c','r','k'])

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()