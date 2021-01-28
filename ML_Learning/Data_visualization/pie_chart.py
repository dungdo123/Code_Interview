import matplotlib.pyplot as plt

slices = [5,7,8,4]
activities = ['eating', 'sleeping', 'working', 'playing']
cols = ['c','m','r','b']

plt.pie(slices,
        labels=activities,
        colors=cols,
        startangle=90,
        shadow=True,
        explode=(0,1,0,0),
        autopct='%1.1f%%')
plt.title('pie chart example')
plt.show()