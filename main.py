from rtlsdr import RtlSdr
import matplotlib.pyplot as plt
import numpy as np

sdr = RtlSdr()

sdr.sample_rate = 2.4e6
sdr.freq_correction = 60
sdr.gain = 'auto'


for i in range(90,110,2):
    sdr.center_freq = i*1e6
    samples = sdr.read_samples(256*1024)
    plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

sdr.close()

plt.xlabel('Freq')
plt.ylabel('dB')
plt.show()
