# Common Part

# Library that we needed

import scipy.io as spio
import scipy.signal as signal
import os
import matplotlib.pyplot as plt
import numpy as np

# Data path linking and declaration

DataPath='C:/SummerSem/TELE/Scripts/Scripts/RAW_exam/'

Files=os.listdir(DataPath)

currentfile=str(DataPath)+str(Files[0])

# importing MATLAB mat file   (containing radar raw data)
mat = spio.loadmat(currentfile, squeeze_me=True)

datenums=mat['datenums']
ranges=mat['ranges']
data=mat['RD']

t=(datenums-np.floor(np.min(datenums)))*24

dl = 6360
du = dl + 1589

t1 = t[dl:du]
datanew = data[:,dl:du,:,0]
datanew.shape
# number of range gates , data points, receivers

noRG=np.size(datanew,0)
noDP=np.size(datanew,1)
noRx=np.size(datanew,2)
#noPol=np.size(datanew,3)

antpo=np.complex64(mat['Antposxy'])
antpos=np.reshape(antpo,(4,))

# task 5

tc = (t1 - min(t1)) * 60 * 60
t2 = -1 * tc[::-1]
t2 = np.append(t2, tc[1:])

# autocor=signal.correlate(data[:,:,0],data[:,:,0])
autocor = np.zeros([noRG, noDP * 2 - 1, noRx]) + 1j * np.zeros([noRG, noDP * 2 - 1, noRx])

for rg in range(noRG):
    autocor[rg, :, 0] = signal.correlate(datanew[rg, :, 0], datanew[rg, :, 0])
    autocor[rg, :, 1] = signal.correlate(datanew[rg, :, 1], datanew[rg, :, 1])

plt.subplot(1, 2, 1)
plt.pcolor(t2, ranges, 10 * np.log10(np.abs(autocor[:, :, 0])), cmap='jet', shading='auto')
plt.xlabel('lag (samples)')
plt.ylabel('range /km')
plt.title('Acor rec1')
plt.clim([20, 90])
plt.subplot(1, 2, 2)
plt.pcolor(t2, ranges, 10 * np.log10(np.abs(autocor[:, :, 1])), cmap='jet', shading='auto')
plt.xlabel('lag (samples)')
plt.ylabel('range /km')
plt.title('Acor rec2')
plt.clim([20, 90])
plt.colorbar()
plt.tight_layout()

plt.figure()
plt.subplot(1, 2, 1)
plt.pcolor(t2, ranges, np.angle(autocor[:, :, 0]) / np.pi * 180, cmap='jet', shading='auto')
plt.clim([-180, 180])
plt.ylabel('range /km')
plt.xlabel('lag (samples)')
plt.title('REC1 - phase /°')
plt.subplot(1, 2, 2)
plt.pcolor(t2, ranges, np.angle(autocor[:, :, 1]) / np.pi * 180, cmap='jet', shading='auto')
plt.clim([-180, 180])
plt.colorbar()
plt.ylabel('range /km')
plt.xlabel('lag (samples)')
plt.title('REC2 - phase /°')
plt.tight_layout()