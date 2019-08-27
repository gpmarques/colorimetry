import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_excel("all_1nm_data.xls", skiprows=range(0, 3))
visible_light_df = df[(df.nm > 379) & (df.nm < 781)]
visible_light_df.describe()
visible_light_df.head(1)  # sanity check


ax = plt.gca()
visible_light_df.plot(kind="line", x="nm", y="CIE D65", ax=ax)
visible_light_df.plot(kind="line", x="nm", y="CIE A", ax=ax)

ax = plt.gca()
visible_light_df.plot(kind="line", x="nm", y="x bar", ax=ax)
visible_light_df.plot(kind="line", x="nm", y="y bar", ax=ax)
visible_light_df.plot(kind="line", x="nm", y="z bar", ax=ax)

ax = plt.gca()
visible_light_df.plot(kind="line", x="nm", y="VM(l)", ax=ax)
visible_light_df.plot(kind="line", x="nm", y="V'(l)", ax=ax)

xyz_to_rgb = np.array([
    [2.36440, -0.89580, -0.46770],
    [-0.51483, 1.42523, 0.08817],
    [0.00520, -0.01440, 1.00921]
])
visible_light_df[['nm', 'x bar', 'y bar', 'z bar']].head(1)
xyz = visible_light_df[['x bar', 'y bar', 'z bar']].to_numpy(dtype=np.float32)
l = visible_light_df["V'(l)"].to_numpy(dtype=np.float32)
cieA = visible_light_df["CIE A"].to_numpy(dtype=np.float32)
XYZ = xyz.T.dot(cieA)
XYZ = XYZ/XYZ[1]
XYZ


x = XYZ[0]/XYZ.sum()
y = XYZ[1]/XYZ.sum()
z = XYZ[2]/XYZ.sum()

rgb = xyz_to_rgb.dot(cieD65XYZ)
rgb[:, 0]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter3D(
    colors[:, 0], colors[:, 1], colors[:, 2],
    facecolors=rgb, edgecolors=np.clip(2*colors - 0.5, 0, 1),
    linewidt=0.5)
ax.set(xlabel='r', ylabel='g', zlabel='b')
