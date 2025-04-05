import matplotlib.pyplot as plt
from random import randrange

fig = plt.figure(layout="constrained")
ax_array = fig.subplots(2, 2, squeeze=False)

x =["1", "2", "3", "4", "5" ]
y_mat = [randrange(1,10) for i in range(5)]
y_fizra = [randrange(1,10) for i in range(5)]
y_vvarkt = [randrange(1,10) for i in range(5)]
y_inza = [randrange(1,10) for i in range(5)]

ax_array[0, 0].bar(x, y_vvarkt,color="green")
ax_array[0, 0].text(1.5,-1.5, "ВВАРКТ")
ax_array[0, 1].bar(x, y_mat,color="blue" )
ax_array[0, 1].text(1.5,-1.5, "Матан")
ax_array[1, 0].bar(x, y_fizra,color="purple" )
ax_array[1, 0].text(1.5,-1.5, "Физра")
ax_array[1, 1].bar(x, y_inza,color="red")
ax_array[1, 1].text(1.5,-1.5, "Инжа")
plt.legend()
plt.show()
