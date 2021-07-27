import scipy.io as spio
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
# import datetime



DataPath = 'C:/SummerSem/TELE/Scripts/Scripts/RAW_exam/'
Files=os.listdir(DataPath)

currentfile=str(DataPath)+str(Files[0])

# importing MATLAB mat file   (containing radar raw data)
mat = spio.loadmat(currentfile, squeeze_me=True)

datenum=mat['datenums']
rang=mat['ranges']
data=mat['RD']

np.shape(data)
data.shape # (ranges, samples, receivers)

# 81 range gates, 7950 time samples, 4 receiver channel, 2 beam directions
# receiver index 0: entire array, 1-3 individual antennas

# perhaps delete mat as soon as you don't need it anymore - freeing memory

plt.figure()
plt.plot(datenum)

# -> multiple experiment runs in the raw data

# for further examination - find the jumps in the time and seperate the individual experiments

# no. range gates, no. data samples, no. receivers, no. polarisations

data=data[:,6360:7949,:,0]
data.shape

ranges=np.reshape(rang,(81,))
datenums=np.reshape(datenum,(7950,))


t=(datenum-np.floor(np.min(datenum)))*24
t=t[6360:7949]


# number of range gates , data points, receivers
noRG=np.size(data,0)
noDP=np.size(data,1)
noRx=np.size(data,2)

pol=1
RXsel=1

i = 1
rg = 0
nocorr = 0

XcorPo = np.zeros([noRG,6])
XcorPh = np.zeros([noRG,6])
XcorMax = np.zeros([noRG,6])
            
xcor=np.zeros([noRG,noDP*2-1,6])+1j*np.zeros([noRG,noDP*2-1,6])


while i <= 3:
    j = 1
    while j <= 3:
        
# cross-correlation for one range and two receivers -> testing reasons
        if i != j:
            

            for rg in range(noRG):
                xcor[rg,:,nocorr]=signal.correlate(data[rg,:,i],data[rg,:,j])
                XcorMax[rg,nocorr] = np.amax(abs(xcor[rg,:,nocorr]))
                res = np.where(abs(xcor[rg,:,nocorr]) == np.amax(abs(xcor[rg,:,nocorr])) )
                XcorPo[rg,nocorr] = abs(xcor[rg,int(res[0]),nocorr])
                XcorPh[rg,nocorr] = np.angle(xcor[rg,int(res[0]),nocorr])   

# line plots for the mean of xcor (along the data points - time )
        
            plt.figure()
            
            plt.subplot(1,3,1)
            plt.plot(XcorMax[:,nocorr],ranges)
#            plt.legend(['Rx2','Rx3','Rx4'])
            plt.xlabel('power /dB')
            plt.grid('on')
            plt.subplot(1,3,2)
            plt.plot(10*np.log10(XcorPo[:,nocorr]),ranges)
#            plt.legend(['1-2','1-3','2-3'])
            plt.xlabel('xcor ampl. /dB')
            plt.title(str(i+1)+' cross corr with '+str(j+1))
            plt.grid('on')
            plt.subplot(1,3,3)
            plt.plot(XcorPh[:,nocorr]/np.pi*180,ranges)
#           plt.legend(['1-2','1-3','2-3'])
            plt.xlabel('phase / °')
            plt.grid('on')
        
        else:
            
            nocorr = nocorr - 1
    
        j = j + 1
        nocorr = nocorr + 1
        
    i = i + 1
 