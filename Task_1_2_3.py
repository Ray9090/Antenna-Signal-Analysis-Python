# -*- coding: utf-8 -*-

import scipy.io as spio
import os
import matplotlib.pyplot as plt
import numpy as np
# import datetime
  

def plotPColour_t(t,pwr, title):
    plt.figure()
    plt.pcolor(t,ranges,pwr,cmap='jet',shading='auto')
    plt.xlabel('time / HH')
    plt.ylabel('range /km')
    plt.title(title)
    plt.clim(20,70)
    plt.colorbar()



DataPath='D:/Python/Uni_HWI/scripts20/RAW_ex2021/'

Files=os.listdir(DataPath)

currentfile=str(DataPath)+str(Files[0])

# importing MATLAB mat file   (containing radar raw data)
mat = spio.loadmat(currentfile, squeeze_me=True)

datenums = mat['datenums']
ranges = mat['ranges']
data = mat['RD']


data.shape # (ranges, samples, receivers)


# datenums ~ days since year 0
# here only the time is important for us -> hours, minutes, seconds
# => fraction / remainder of the integer

t=(datenums-np.floor(np.min(datenums)))*24

# number of range gates , data points, receivers

noRG = np.size(data,0)
noDP = np.size(data,1)
noRx = np.size(data,2)
noPol = np.size(data,3)



RXsel   = 0
RG      = -1
pol     = [0,1]


# TASK 1

# 1590 , 3180 , 4770 , 6360

for i in range(noPol):
    dl      = 0
    while dl <= 6360:
        du = dl + 1589
        
        t1 = t[dl:du]
        t1.shape
        
        y = data[:,dl:du,RXsel,i]
        y.shape
        
        PWR = 20*np.log10(np.abs(y))
        type(PWR)
        PWR.shape  

# power plot for all samples and all ranges (altitude)

        plotPColour_t(t1,PWR, str('power /dB for data between '+str(dl)+' & '+str(du)+' & pol : '+str(i))) 
       
        dl = du + 1

## Chosen data step for later tasks [6360:7949]

dl = 6360
du = dl + 1589

t1 = t[dl:du]
data = data[:,dl:du,:,:]

# TASK 2    

data0   = data[:,:,0,0]
data123 = data[:,:,1:4,0]

data.shape
data123.shape
# Combining data for receivers 2,3,4

datacomb = np.sum(data123,2) / 3

# Power for the combined receivers in log-scale

PWR234  = 20*np.log10(np.abs(datacomb)) 

# Power for receiver 0

PWR0    = 20*np.log10(np.abs(data0))

# Plot graphs

plotPColour_t(t1,PWR234,str('combined power /dB for receivers 2,3 & 4'))
plotPColour_t(t1,PWR0,str('Power /dB for receiver 1'))

      

# TASK 3

# perform coherent integrations
def make_ci(t, y, ci):
    nptsn=int(np.floor(len(y)/ci))
    yn=np.empty(nptsn)+1j*np.empty(nptsn)
    tn=np.empty(nptsn)
    for i in range(0,nptsn):
        yn[i]=np.mean(y[i*ci:i*ci+ci-1])
        tn[i]=np.mean(t[i*ci:(i+1)*ci])
    return tn,yn

# make FFT spectrum, frequency axis
def make_fft(t,y):
    dt = t[1]-t[0] # dt -> temporal resolution ~ sample rate
    f = np.fft.fftfreq(t.size, dt) # frequency axis
    Y = np.fft.fft(y)   # FFT
    f=np.fft.fftshift(f)
    Y= np.fft.fftshift(Y)/(len(y))
    return f,Y




noDP=np.size(data,1)

# number of coherent integrations of I/Q raw data (time series)

ci = 14

y=data[3,:,0,0]

tn,yn=make_ci(t,y,ci)

plt.figure()
plt.subplot(1,2,1)
plt.plot(np.real(y),np.imag(y),'*')
plt.xlim([-100,100])
plt.ylim([-100,100])

plt.subplot(1,2,2)
plt.plot(np.real(yn),np.imag(yn),'*')
plt.xlim([-100,100])
plt.ylim([-100,100])

# length of the "new" integrated time series

noDPn = int(np.floor(noDP/ci))

# predefine matrix for integrated raw data

datan = np.zeros([noRG,noDPn,noRx])+1j*np.zeros([noRG,noDPn,noRx])

for rx in range(noRx):
    for rg in range(noRG):
        tn,datan[rg,:,rx]=make_ci(t1,data[rg,:,rx],ci)

# time vector in s

tsec=t1*60*60
tnsec=tn*60*60

# Spectra for all ranges and all receivers

Spectr = np.zeros([noRG,noDP,noRx])+1j*np.zeros([noRG,noDP,noRx])

for rx in range(noRx):
    for rg in range(noRG):
        f,Spectr[rg,:,rx]=make_fft(tsec,data[rg,:,rx,0])

# Spectra for all ranges and all receivers integrated time series

Spectrn=np.zeros([noRG,noDPn,noRx])+1j*np.zeros([noRG,noDPn,noRx])

for rx in range(noRx):
    for rg in range(noRG):
        fn,Spectrn[rg,:,rx]=make_fft(tnsec,datan[rg,:,rx])

plt.figure()
for rx in range(noRx):
    plt.subplot(2,3,rx+1)
    ampl=10*np.log10(abs(Spectr[:,:,rx]))
    SNRsel=ampl<-5   
    ampl[SNRsel]="nan"
    plt.pcolor(f,ranges,ampl,cmap='jet',shading='auto')
    plt.clim([-5, 25])
    plt.xlim([min(fn), max(fn)])
    plt.xlabel('f /Hz')
    plt.ylabel('range /km')
    plt.title('Before CI')
    # plt.colorbar()
    
plt.figure()    
for rx in range(noRx):
    plt.subplot(2,3,rx+1)
    ampln=10*np.log10(abs(Spectrn[:,:,rx]))
    SNRsel=ampln<-5   
    ampln[SNRsel]="nan"
    plt.pcolor(fn,ranges,ampln,cmap='jet',shading='auto')
    plt.clim([-5, 25])
    plt.xlabel('f /Hz')
    plt.ylabel('range /km')
    plt.title('After CI')