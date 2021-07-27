# -*- coding: utf-8 -*-

import scipy.io as spio
import os
import matplotlib.pyplot as plt
from PyAstronomy import pyasl
import numpy as np
#from numpy.fft import fft, ifft, fftshift
# import datetime



DataPath='D:/Python/Uni_HWI/scripts20/RAW_ex2021/'
Files=os.listdir(DataPath)

currentfile=str(DataPath)+str(Files[0])

# importing MATLAB mat file   (containing radar raw data)
mat = spio.loadmat(currentfile, squeeze_me=True)

datenums=mat['datenums']
ranges=mat['ranges']
data=mat['RD']

np.shape(data)
data.shape # (ranges, samples, receivers)

# 81 range gates, 7950 time samples, 4 receiver channel, 2 beam directions
# receiver index 0: entire array, 1-3 individual antennas
# perhaps delete mat as soon as you don't need it anymore - freeing memory

plt.figure()
plt.plot(datenums)

# -> multiple experiment runs in the raw data

# for further examination - find the jumps in the time and seperate the individual experiments

# no. range gates, no. data samples, no. receivers, no. polarisations

data1=data[:,3180:4769,:,0]

t=(datenums-np.floor(np.min(datenums)))*24
t1=t[3180:4769]
# number of range gates , data points, receivers
noRD=np.size(data,0)
noDP=np.size(data,1)
noRx=np.size(data,2)
noPol=np.size(data,3)

pol=0
RXsel=0

def make_fft(t,y):
    dt = t[1]-t[0] # dt -> temporal resolution ~ sample rate
    f = np.fft.fftfreq(t.size, dt) # frequency axis
    Y = np.fft.fft(y)   # FFT
    f=np.fft.fftshift(f)
    Y= np.fft.fftshift(Y)/(len(y))
    return f,Y

tsec=t*60*60

t1=tsec[3180:4769]
f,spec=make_fft(t1,data1[22,:,0])


plt.figure()
plt.plot(f,10*np.log10(abs(spec)))
plt.grid ('on')
plt.xlabel('f / Hz')
plt.ylabel('amplitude /dB')





# Spectra for all ranges for reciever 1


Spectr=np.zeros([noRD,1589])+1j*np.zeros([noRD,1589])

rx=0;
for rg in range(noRD):
    f,Spectr[rg,:] = make_fft(t1,data1[rg,:,rx])


plt.figure()
plt.pcolor(f,ranges,10*np.log10(abs(Spectr[:,:])),cmap='jet',shading='auto')
plt.title('spectra for Reciever 1')
plt.clim([-15, 15])
plt.xlabel('f /Hz')
plt.ylabel('range /km')
plt.xlim([-1,1])
plt.colorbar()

Spectrn = Spectr[20,:]
# ... a gradient in the continuum ...
flux = np.ones([20,1589]) + (Spectr[20,:]/Spectr.min())*0.05
#gaussian distribution

flux -= np.exp(-(Spectr[20,:])*2/(2.*0.5*2))*0.05

plt.title("gaussian distribution")
plt.plot(flux)
plt.show()

# Shift that spectrum redward by 20 km/s using
# "firstlast" as edge handling method.
nflux1, wlprime1 = pyasl.dopplerShift(Spectrn.sort(), flux, 20, edgeHandling="firstlast")

#flux[0,:].shape
#(Spectr/Spectr.min()).shape
# Shift that spectrum redward by 20 km/s using
# "firstlast" as edge handling method.
nflux1, wlprime1 = pyasl.dopplerShift(Spectr, flux, 20., edgeHandling="firstlast")

# Shift the red-shifted spectrum blueward by 20 km/s, i.e.,
# back on the initial spectrum.
nflux2, wlprime = pyasl.dopplerShift(Spectr, nflux1, -20.,
                                     edgeHandling="fillValue", fillValue=1.0)

# Check the maximum difference in the central part
indi = np.arange(len(flux)-200) + 100
print("Maximal difference (without outer 100 bins): ",
      max(np.abs(flux[indi]-nflux2[indi])))

# Plot the outcome
plt.title("Initial (blue), shifted (red), and back-shifted (green) spectrum")
plt.plot(Spectr, flux, 'b.-')
plt.plot(Spectr, nflux1, 'r.-')
plt.plot(Spectr, nflux2, 'g.-')
plt.show()