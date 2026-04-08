#bandwidh 
import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy.datasets import electrocardiogram

#--contaminada
ecg_full=electrocardiogram()
Fs=360
N=4000
t=np.arange(N)/Fs
ecg_clean=ecg_full[:N]
#a baseline drift y ruido
ecg_contaminated=ecg_clean+0.5*np.sin(2*np.pi*.03*t)+0.08*np.random.randn(N)

#substraccion
wavelet="sym10"
Fc=0.5
desired_lev=int(np.ceil(np.log2(Fs/Fc)))
maxlev=pywt.dwt_max_level(N,pywt.Wavelet(wavelet).dec_len)
lev=min(desired_lev,maxlev)
coeffs=pywt.wavedec(ecg,wavelet,level=lev)
coeffs_approx =[coeffs[0]]+[np.zeros_like(x) for x in coeffs[1:]]
baseline=pywt.waverec(coeffs_approx,wavelet)[:N]
ecg_wavelet_baseline=ecg-baseline
#show

# plt.plot(t,ecg)
# plt.xlabel('Tiempo (s)')
# plt.ylabel('ecg in mv')
# plt.xlim(9,10.2)
# plt.ylim(-1,1.5)
# plt.show()


#plot the clean and contaminated
plt.figure(figsize=(12,6))
plt.plot(t,ecg_clean,label='clean',color='blue',linewidth=2)
plt.plot(t,ecg_contaminated,label='contaminated',color='red',alpha=0.5,linewidth=2)
plt.plot()
plt.title('limpiovs sucio')
plt.xlabel('Tiempo (s)')
plt.ylabel('ecg in mv')

plt.legend()
plt.grid(True)
plt.show()


#plot the extracted baseline

plt.figure(figsize=(12,6))
plt.plot(t,ecg_contaminated,label='contaminated',color='red',linewidth=2)

plt.plot(t,baseline,label='baseline',color='green',linewidth=2)
plt.plot()
plt.title('baseline vs contaminada')
plt.xlabel('Tiempo (s)')
plt.ylabel('ecg in mv')
plt.legend()
plt.grid(True)
plt.show()

#substrallendo the baseline to get the denoised
ecg_wavelet_baseline=ecg_contaminated-baseline

plt.figure(figsize=(12,6))

plt.plot(t,ecg_wavelet_baseline,label='ecg_wavelet_baseline',color='green',linewidth=2)
plt.plot()
plt.title('final')
plt.xlabel('Tiempo (s)')
plt.ylabel('ecg in mv')
plt.legend()
plt.grid(True)
plt.show()
