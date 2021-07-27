# Common Part

# Library that we needed

import scipy.io as spio
import scipy.signal as signal
import os
import matplotlib.pyplot as plt
import numpy as np

# Data path linking and declaration

DataPath='D:/Python/Uni_HWI/scripts20/RAW_ex2021/'

Files=os.listdir(DataPath)

currentfile=str(DataPath)+str(Files[0])

# importing MATLAB mat file   (containing radar raw data)
mat = spio.loadmat(currentfile, squeeze_me=True)

datenums=mat['datenums']
ranges=mat['ranges']
data=mat['RD']

t=(datenums-np.floor(np.min(datenums)))*24

# number of range gates , data points, receivers

dl = 6360
du = dl + 1589

t1 = t[dl:du]
datanew = data[:,dl:du,:,:]

# number of range gates , data points, receivers

noRG=np.size(datanew,0)
noDP=np.size(datanew,1)
noRx=np.size(datanew,2)
noPol=np.size(datanew,3)

antpo=np.complex64(mat['Antposxy'])
antpos=np.reshape(antpo,(4,))

# task 5

tc = (t1 - min(t)) * 60 * 60
t2 = -1 * tc[::-1]
t2 = np.append(t2, tc[1:])


# Task 8

wl=92.896

RXPhases=[0, -15.7, -24.4, 0, 6.65, -6.73, 26.67, 11.92, 10.58]
RXPhases=np.mat(RXPhases)*-1/180*np.pi
for rx in range (noRx):
    datanew[:,:,rx,0]=datanew[:,:,rx,0]*np.exp(1j*RXPhases[0,rx+5])

datamean=np.mean(datanew[:,:,:,0],1)

pairs=[[1,2],[1,3],[2,3]]

nopairs=np.size(pairs,0)

dx=np.zeros([nopairs])
dy=np.zeros([nopairs])
phases=np.zeros([noRG,nopairs])

for pp in range(nopairs):
    dx[pp]=(antpos[pairs[2][0]]-antpos[pairs[pp][1]]).real
    dy[pp]=(antpos[pairs[2][0]]-antpos[pairs[pp][1]]).imag
    phases[:,pp]=np.angle(datamean[:,pairs[pp][0]]*np.conjugate(datamean[:,pairs[pp][1]]))

R=2*np.pi/wl * np.array([dx, dy])

R=R.T

B=np.matmul(np.mat(R).T,np.mat(R))


pos_data=np.zeros([noRG,2])
phi=np.zeros([noRG,1])
theta=np.zeros([noRG,1])


for rg in range(noRG):
    b=np.matmul(np.mat(R).T,np.mat(phases[rg,:]).T)
    r=np.linalg.solve(B.T.dot(B), B.T.dot(b))
    pos_data[rg,:]=r.T
    phi[rg]=np.arctan2(r[1],r[0])/np.pi*180
    theta[rg]=np.arcsin(np.sqrt(r[0]**2+r[1]**2))/np.pi*180

plt.subplot(2, 1, 1)
plt.plot(pos_data[15:,0],pos_data[15:,1],'.')
plt.xlim([-1,1])
plt.ylim([-1,1])
plt.grid(1)
plt.xlabel('dcosx sin(theta)cos(phi)')
plt.ylabel('dcosy sin(theta)sin(phi)')

plt.subplot(2, 1, 2)
plt.plot(phi,ranges)
plt.plot(theta,ranges)
plt.legend(('phi','theta'))
plt.title('AOA')