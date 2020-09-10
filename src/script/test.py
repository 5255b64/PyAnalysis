import math

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-2 * math.pi, 2 * math.pi, 0.02)
y = np.sin(x)

plt.axis([-10, 10, -2, 2])

plt.xticks([i * np.pi/2 for i in range(-4, 5)], [str(i * 0.5) + "$\pi$" for i in range(-4, 5)])

plt.yticks([i * 0.5 for i in range(-4, 5)])

plt.xlabel("x")
plt.ylabel("y")

plt.plot(x, y, color="r", linestyle="-", linewidth=1)

plt.show()