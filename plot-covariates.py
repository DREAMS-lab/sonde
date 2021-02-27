import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('20210226-042549-dreams-manta.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[3]))
        y.append(float(row[4]))

N = len(x)
print(N)
plt.plot(x,y,'.')
plt.plot(x[0],y[0],'r.',label='start')
plt.plot(x[N-1],y[N-1],'rx', label='current')

plt.xlabel('temperature (deg C)')
plt.ylabel('pH')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()
