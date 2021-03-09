import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
from scipy import interpolate

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
            datestr = tokens[0]+' '+tokens[1]
            unixtime = time.mktime(datetime.datetime.strptime(datestr,"%m/%d/%y %H:%M:%S").timetuple())
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

latvecF = interpolate.interp1d(gps_nparr[:,0], gps_nparr[:,1],fill_value="extrapolate")
latvec = latvecF(sonde_nparr[:,0])

lonvecF = interpolate.interp1d(gps_nparr[:,0], gps_nparr[:,2],fill_value="extrapolate")
lonvec = lonvecF(sonde_nparr[:,0])


NUM=9
fig,ax = plt.subplots(NUM)

for i in range(NUM):
    pl = ax[i].scatter(lonvec, latvec,c=sonde_nparr[:,i+3],s=5)
    ax[i].set_xlim([-111.91497219999999, -111.9146689])
    ax[i].set_ylim([33.375203300000003,33.3756117])
    fig.colorbar(pl, ax=ax[i])

plt.show()
print("done!")

