#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

f = 0.08
h = 0.24
lift = 0.03
span = 0.25

ground = 0.06
pathrange = 10

L = []
for j in range(pathrange):
    div = (f)/pathrange     
    x = span + div*j 
    z = np.sqrt(lift**2 * (1 - (2*(x-span-f/2)/f)**2))
    L.append([x, 0.0, z])
L.append([span+f, 0.0, 0])

# Extract coordinates for plotting
X, Y, Z = zip(*L)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z, c='r', marker='o')
ax.set_zlim([0.0, 0.1])

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('3D Plot of Points')

plt.show()
