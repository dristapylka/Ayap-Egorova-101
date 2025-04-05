import matplotlib.pyplot as plt
from numpy import arange
from random import uniform
import statistics
x = [1, 2, 3, 4, 5]
y = [i*2 for i in x]
y_i=[]
x_i=[]
for i in range(5):
    x_i.append([uniform(x[i]-0.5, x[i]+0.5) for k in range(5)])
    y_i.append([uniform(y[i]-0.5, y[i]+0.5) for k in range(5)])

plt.xticks(arange(0,5,0.5))
plt.yticks(arange(0,15,0.5))

for k in range(5):
    plt.scatter(x_i[k],y_i[k])

x_c=[statistics.mean(i) for i in x_i]
y_c=[statistics.mean(i) for i in y_i]

x_er=[abs((sum(x_i[v])-5*x[v])/5) for v in range(5)]
y_er=[abs((sum(y_i[v])-5*y[v])/5) for v in range(5)]
plt.errorbar(x_c,y_c, yerr=y_er,xerr=x_er,fmt='o')
print(x_er)

plt.scatter(x_c,y_c)

plt.show()