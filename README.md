# Antenna-Signal-Analysis-Python
Antenna Signal Analysis, Perform various calculation using Python 

The main role of the project deals with the RADAR raw data analysis and signal processing for all range gates. The multiple aims of the project are, plotting
the power and spectra of the raw data for all range gates, application of coherent integration, performing auto and cross-correlation, calculation of the
angle-of-arrival .

Main target to perform auto-correlation, corss-correlation, discuss about power distribution, Power Spectral Density, Fast Fourior Transform, Coherent Integration, Angle of Arrival,  

Tasks for this project
version June 18th 

> RAW data analysis and signal processing <

1) Plot the power of the raw data for all range gates, temporal samples and both polarisation, but only receiver 1 (index 0)
	-> e.g. pcolor plots
	-> select ONE interesting raw data portion (one experiment run), where most echoes are visible, 
	-> use this selected data for all the subsequent tasks!

2) Spectra over range for the receiver channel 1 and the spectral average of channel 2-4
	-> e.g. pcolor plots

3) Apply a suitable number of either coherent integrations or incoherent integration (Low pass filter version)
	-> show resulting spectra, equivalently to task 2)

4) Derive the spectral width of the observed spectra for receiver 1 after applying integrations
	-> assume a gaussian distribution, fit this gaussian (varying the position (Doppler shift) and width
	-> plot the width and found Doppler shift along the ranges  (line plots)

5) Show the autocorrelation for receiver 1 and one of the other for all ranges
	-> e.g. 2x pcolor figure

6) Perfom the crosscorrelation for all combinations of receiver channel 2-4 
	find the maximum amplitude 
	show in a line plot the position of found maximum, 
	as well as corresponding amplitudes and phases for each range

7) Show the cross-spectra for all combinations of receiver channel 2-4 in amplitude and phase, 
	apply suitable SNR-cleaning for beautiful figure

8) Calculate the angle-of-arrival for all ranges using receiver channel 2-4
	plot the found positions, apply suitable SNR-cleaning 

Fig1. Power graphs for Rx 1 for all range gates for each step of data and
polarisation.

![task 1 1](https://user-images.githubusercontent.com/58274552/127184564-35bbd882-2cd4-4277-86bf-8f3dd19a86e5.PNG)



![task 1 2](https://user-images.githubusercontent.com/58274552/127184594-bfebb74d-ae96-4df7-badc-46700f7ae942.PNG)




![task 1 3](https://user-images.githubusercontent.com/58274552/127184888-f62f0695-1561-484d-8ea5-d44fa5a32e50.PNG)



Fig2. Power graphs of Receiver 1 and the average of Receiver 2,3 & 4.



![task 2](https://user-images.githubusercontent.com/58274552/127185433-c4ff6d0b-6912-4624-914e-f4fdf518ed07.PNG)



Fig3: Spectra for all receivers before and after Integration



![task 3](https://user-images.githubusercontent.com/58274552/127185712-6365775a-d573-4719-8fea-f40b9308bf8c.PNG)



Fig4: Power and Phase graphs for autocorrelation



![task 5](https://user-images.githubusercontent.com/58274552/127185830-74fdbc7c-2336-4027-b4a8-470c07ed0aa0.PNG)



Fig5: Cross-Correlation of all the gates for selected data



![task 6](https://user-images.githubusercontent.com/58274552/127185970-f1812ad0-dc63-4afe-bf28-2d24c5aa3d66.PNG)



Fig6. Cross- spectra after SNR thresholding



![task 7](https://user-images.githubusercontent.com/58274552/127186116-e57ec9bc-c93a-4167-98e8-086690bc4a25.PNG)



Fig7. Angle of arrival for Channel 2-4



![task 8](https://user-images.githubusercontent.com/58274552/127186203-33cd18af-e6a1-4bd3-bfad-88acace71a4e.PNG)





