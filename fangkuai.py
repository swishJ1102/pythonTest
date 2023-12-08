import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

vertices = [
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
]

faces = [
    [vertices[0], vertices[1], vertices[5], vertices[4]],
    [vertices[7], vertices[6], vertices[2], vertices[3]],
    [vertices[0], vertices[4], vertices[7], vertices[3]],
    [vertices[1], vertices[5], vertices[6], vertices[2]],
    [vertices[4], vertices[5], vertices[6], vertices[7]],
    [vertices[0], vertices[1], vertices[2], vertices[3]]
]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_zticks([0, 1])

plt.show()
