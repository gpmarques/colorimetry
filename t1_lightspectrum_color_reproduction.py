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
xyzbar = visible_light_df[['x bar', 'y bar', 'z bar']].to_numpy(
    dtype=np.float32)
xyzbar.shape
radiance = visible_light_df["VM(l)"].to_numpy(dtype=np.float32)
radiance.shape
cieA = visible_light_df["CIE A"].to_numpy(dtype=np.float32)

XYZ = xyzbar.T.dot(radiance)
XYZ = XYZ/XYZ[1]
XYZ

xyz = XYZ / XYZ.sum()
print(xyz)

rgb = xyz_to_rgb.dot(xyz)
print(rgb)
