import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y1 = [i for i in x]
y2 = [i*2 for i in x]
y3 = [i*3 for i in x]
y4 = [i**2 for i in x]
y5 = [2*(i**2) for i in x]
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)
plt.plot(x, y4)
plt.plot(x, y5)
plt.show()
