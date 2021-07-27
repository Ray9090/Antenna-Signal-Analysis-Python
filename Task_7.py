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

def make_fft(t,y):
    dt = t[1]-t[0] 
    f = np.fft.fftfreq(t.size, dt) 
    Y = np.fft.fft(y)   
    f=np.fft.fftshift(f)
    Y= np.fft.fftshift(Y)/(len(y))
    return f,Y

tc = (t1 - min(t1)) * 60 * 60

Spectr=np.zeros([noRG, noDP , noRx]) + 1j * np.zeros([noRG, noDP , noRx])

for rg in range(noRG):
        f,Spectr[rg,:,1]=make_fft(tc,datanew[rg,:,1])
for rg in range(noRG):
        f,Spectr[rg,:,2]=make_fft(tc,datanew[rg,:,2])
for rg in range(noRG):
        f,Spectr[rg,:,3]=make_fft(tc,datanew[rg,:,3])
        
plt.subplot(1,3,1)        
plt.pcolor(f,ranges,10*np.log10(abs(Spectr[:,:,1])),cmap='jet',shading='auto')
plt.xlabel('f /Hz')
plt.ylabel('range /km')
plt.title('spec2')
plt.clim([-15,15])
plt.subplot(1,3,2)
plt.pcolor(f,ranges,10*np.log10(abs(Spectr[:,:,2])),cmap='jet',shading='auto')
plt.xlabel('f /Hz')
plt.ylabel('range /km')
plt.title('spec3')
plt.clim([-15,15])
plt.subplot(1,3,3)
plt.pcolor(f,ranges,10*np.log10(abs(Spectr[:,:,3])),cmap='jet',shading='auto')
plt.xlabel('f /Hz')
plt.ylabel('range /km')
plt.title('spec4')
plt.clim([-15,15])
plt.colorbar()
plt.tight_layout()

XSpectr=np.zeros([noRG, noDP , noRx]) + 1j * np.zeros([noRG, noDP , noRx])

XSpectr[:,:,1]=Spectr[:,:,1]*np.conj(Spectr[:,:,2])
XSpectr[:,:,2]=Spectr[:,:,1]*np.conj(Spectr[:,:,3])
XSpectr[:,:,3]=Spectr[:,:,2]*np.conj(Spectr[:,:,3])

plt.suptitle('Before SNR thresholding')
plt.subplot(2,3,1)
plt.pcolor(f,ranges,10*np.log10(abs(XSpectr[:,:,1])/2),cmap='jet')
plt.title('XSp ampl[2,3]')
plt.clim([-15,15])
plt.subplot(2,3,2)
plt.pcolor(f,ranges,10*np.log10(abs(XSpectr[:,:,2])/2),cmap='jet')
plt.title('XSp ampl[2,4]')
plt.clim([-15,15])
plt.subplot(2,3,3)
plt.pcolor(f,ranges,10*np.log10(abs(XSpectr[:,:,3])/2),cmap='jet')
plt.title('XSp ampl[3,4]')
plt.clim([-15, 15])
plt.colorbar() 
plt.tight_layout()

phases=[]

plt.subplot(2,3,4)
phases=np.angle(XSpectr[:,:,1])/np.pi*180
plt.pcolor(f,ranges,phases,cmap='jet',shading='auto')
plt.title('XSp phase[2,3]')
plt.clim([-180, 180]) 
plt.subplot(2,3,5)
phases=np.angle(XSpectr[:,:,2])/np.pi*180
plt.pcolor(f,ranges,phases,cmap='jet',shading='auto')
plt.title('XSp phase[2,4]')
plt.clim([-180, 180])
plt.subplot(2,3,6)
phases=np.angle(XSpectr[:,:,3])/np.pi*180
plt.pcolor(f,ranges,phases,cmap='jet',shading='auto')
plt.clim([-180, 180])
plt.colorbar()
plt.title('XSp phase[3,4]')
plt.tight_layout()

# SNR CLEANING
plt.suptitle('After SNR thresholding')
plt.subplot(2,3,1)        
ampl=10*np.log10(abs(XSpectr[:,:,1])/2)
SNRsel=ampl<-8
ampl[SNRsel]="nan"
plt.pcolor(f,ranges,ampl,cmap='jet',shading='auto')
plt.title('XSp ampl[2,3]')
plt.clim([-15, 15])
plt.subplot(2,3,2)
ampl=10*np.log10(abs(XSpectr[:,:,2])/2)
SNRsel=ampl<-8
ampl[SNRsel]="nan"
plt.pcolor(f,ranges,ampl,cmap='jet',shading='auto')
plt.title('XSp ampl[2,4]')
plt.clim([-15, 15])
plt.subplot(2,3,3)
ampl=10*np.log10(abs(XSpectr[:,:,3])/2)
SNRsel=ampl<-8
ampl[SNRsel]="nan"
plt.pcolor(f,ranges,ampl,cmap='jet',shading='auto')
plt.title('XSp ampl[3,4]')
plt.clim([-15, 15])
plt.colorbar()
plt.tight_layout()

plt.subplot(2,3,4)
phases=np.angle(XSpectr[:,:,1])/np.pi*180
SNRsel=10*np.log10(abs(XSpectr[:,:,1])/2)<-8
phases[SNRsel]="nan"
plt.pcolor(f,ranges,phases,cmap='jet',shading='auto')
plt.title('XSp phase[2,3]')
plt.clim([-180, 180])
plt.subplot(2,3,5)        
phases=np.angle(XSpectr[:,:,2])/np.pi*180
SNRsel=10*np.log10(abs(XSpectr[:,:,2])/2)<-8
phases[SNRsel]="nan"
plt.pcolor(f,ranges,phases,cmap='jet',shading='auto')
plt.title('XSp phase[2,4]')
plt.clim([-180, 180])
plt.subplot(2,3,6)        
phases=np.angle(XSpectr[:,:,3])/np.pi*180
SNRsel=10*np.log10(abs(XSpectr[:,:,3])/2)<-8
phases[SNRsel]="nan"
plt.pcolor(f,ranges,phases,cmap='jet',shading='auto')
plt.title('XSp phase[3,4]')
plt.clim([-180, 180])
plt.colorbar()
plt.tight_layout()
