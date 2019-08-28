import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    [2.0413690, -0.5649464, -0.3446944],
    [-0.9692660, 1.8760108, 0.0415560],
    [0.0134474, -0.1183897, 1.0154096]
])
xyzbar = visible_light_df[['x bar', 'y bar', 'z bar']].to_numpy(
    dtype=np.float32)
xyzbar.shape
xyzbar
cieA = visible_light_df["CIE A"].to_numpy(dtype=np.float32)
cieD65 = visible_light_df["CIE D65"].to_numpy(dtype=np.float32)
#  normalize
cieD65 = (cieD65 - cieD65.min()) / (cieD65.max() - cieD65.min())
cieD65.shape

spectra_df = pd.read_excel(
    "ColorChecker_RGB_and_spectra.xls",
    sheet_name="spectral_data", skiprows=range(0, 1), nrows=24)
spectra_df.tail(1)

spectral_data = spectra_df.loc[:, spectra_df.columns[2:]].to_numpy(
    dtype=np.float32)
spectral_data.shape
wavelengths_index = [i for i in range(0, 360, 10)]
LB = (cieD65[wavelengths_index] * spectral_data).T
XYZ = xyzbar[wavelengths_index].T.dot(LB)
XYZ = XYZ / XYZ[1]
XYZ.shape
rgb = xyz_to_rgb.dot(XYZ)
rgb.shape
y, x = np.array([(i, j) for i in range(4) for j in range(6)]).T
plt.scatter(x, y, c=np.clip(rgb, 0, 1).T, s=1500)
