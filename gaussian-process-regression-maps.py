#!/usr/bin/env python3
import datetime
import time
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

np.random.seed(1)
sondefile = '20210308-093511-dreams-manta-cleaned.csv'
gpsfile = 'navfix-log.txt'

line = True
gps_vec = []
sonde_vec = []

with open(sondefile) as fp:
    while line:
        line = fp.readline().rstrip()
        tokens = line.split(',')
        if len(tokens) == 12:
            datestr = tokens[0] + ' ' + tokens[1]
            unixtime = time.mktime(datetime.datetime.strptime(datestr, "%m/%d/%y %H:%M:%S").timetuple())
            tokens[0] = unixtime
            tokens[1] = 0
            sonde_vec.append(np.array(tokens, dtype=float))
fp.close()

line = True
with open(gpsfile) as fp:
    line = fp.readline().rstrip()
    while line:
        line = fp.readline().rstrip()
        tokens = line.split(',')
        if len(tokens) == 19:
            timesec = tokens[0][:10]
            timensec = tokens[0][10:]
            time_float = float(str(timesec) + '.' + str(timensec))
            tokens_proc = [time_float, tokens[6], tokens[7], tokens[8], tokens[9]]
            data_list = np.array(tokens_proc, dtype=float)
            gps_vec.append(data_list)
gps_nparr = np.array(gps_vec, dtype=float)
sonde_nparr = np.array(sonde_vec, dtype=float)

plot_title = \
    ['Temp_deg_C',
     'pH_units',
     'Depth_m',
     'SpCond_uS/cm',
     'Turb_FNU',
     'HDO_%Sat',
     'HDO_mg/l',
     'Chl_ug/l',
     'CDOM_ppb']

min_boat_time = np.min(gps_nparr[:, 0])
max_boat_time = np.max(gps_nparr[:, 0])

sonde_nparr = sonde_nparr[sonde_nparr[:, 0] < max_boat_time]
latvecF = interpolate.interp1d(gps_nparr[:, 0], gps_nparr[:, 1], fill_value="extrapolate")
latvec = latvecF(sonde_nparr[:, 0])

lonvecF = interpolate.interp1d(gps_nparr[:, 0], gps_nparr[:, 2], fill_value="extrapolate")
lonvec = lonvecF(sonde_nparr[:, 0])

xx = [lonvec, latvec]
SONDE_PARAM = 0

X = (np.array([lonvec, latvec])).T
y_obs = np.array(sonde_nparr[:, SONDE_PARAM + 3])
kernel = RBF()
gp = GaussianProcessRegressor(kernel=kernel)
gp.fit(X, y_obs)
print("Learned kernel", gp.kernel_)

res = 500
lin_lat = np.linspace(33.375203300000003, 33.3756117, res)
lin_lon = np.linspace(-111.91497219999999, -111.9146689, res)
x1x2 = np.array(list(product(lin_lon, lin_lat)))
WIDTH = 1
y_pred, MSE = gp.predict(x1x2, return_std=True)
_vmax = np.median(y_pred) + WIDTH * np.std(y_pred)
_vmin = np.median(y_pred) - WIDTH * np.std(y_pred)
GRID_N = res
X0p, X1p = x1x2[:, 0].reshape(GRID_N, GRID_N), x1x2[:, 1].reshape(GRID_N, GRID_N)
Zp = np.reshape(y_pred, (GRID_N, GRID_N))
plt.pcolormesh(X0p, X1p, Zp, vmax=18.7, vmin=18.3)
plt.colorbar(extend='max')
plt.tight_layout()
plt.figure()
Zpmse = np.reshape(MSE, (GRID_N, GRID_N))

plt.pcolormesh(X0p, X1p, Zpmse)
plt.colorbar(extend='max')

plt.show()
