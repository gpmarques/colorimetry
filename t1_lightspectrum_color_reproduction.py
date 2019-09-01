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
    [3.240710, -1.537260, -0.498571],
    [-0.969258, 1.875990, 0.041556],
    [0.055635, -0.203996, 1.057070]
])

cieD65 = visible_light_df["CIE D65"].to_numpy(dtype=np.float32)
xyzbar = visible_light_df[['x bar', 'y bar', 'z bar']].to_numpy(
    dtype=np.float32)
xyzbar.shape
xyzbar[0, :]

spectra_df = pd.read_excel(
    "ColorChecker_RGB_and_spectra.xls",
    sheet_name="spectral_data", skiprows=range(0, 1), nrows=24)
spectra_df.tail(1)

spectral_data = spectra_df.loc[:, spectra_df.columns[2:]].to_numpy(
    dtype=np.float32)
spectral_data.shape


def spectral_to_rgb(spectral_data, illuminant, xyz_to_rgb):
    wavelengths_index = [i for i in range(0, 360, 10)]
    LB = (illuminant[wavelengths_index] * spectral_data).T
    XYZ = xyzbar[wavelengths_index].T.dot(LB)
    k = illuminant[wavelengths_index].dot(xyzbar[wavelengths_index, 1])
    XYZ = XYZ / k
    rgb = xyz_to_rgb.dot(XYZ)
    y, x = np.array([(i, j) for i in range(4) for j in range(6)]).T
    plt.scatter(x, y, c=np.clip(rgb, 0, 1).T, s=1500)


spectral_to_rgb(spectral_data, cieD65, xyz_to_rgb)
