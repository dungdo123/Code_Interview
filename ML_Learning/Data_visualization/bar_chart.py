import matplotlib.pyplot as plt

population_ages = [5,10,15,20,25,30,35,45,50,80]
bins = [0,10,20,30,40,50,60,70,80,90,100]
plt.hist(population_ages, bins,histtype='bar',rwidth=0.5)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting graph')
#plt.legend("hahaha")
plt.show()