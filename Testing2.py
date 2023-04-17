import numpy as np
import matplotlib.pyplot as plt
import time
from rtlsdr import RtlSdr

# configure SDR
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 140e6
sdr.gain = 'auto'

Fs = sdr.sample_rate
Ts = 1/Fs # sample period
N = 256*1024
noise_power = 2

# create the figure and axis for the plot
fig, ax = plt.subplots()
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("Magnitude [dB]")

ax.grid(True)

while True:
    samples = sdr.read_samples(N)
    PSD = np.abs(np.fft.fft(samples))**2 / (N*Fs)
    PSD_log = 10.0*np.log10(PSD)
    PSD_shifted = np.fft.fftshift(PSD_log)
    print(PSD_shifted)

    f = np.arange(-Fs/2, Fs/2, Fs/N) # start, stop, step

    # update the data for the plot
    ax.clear()
    ax.plot(f, PSD_shifted)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Magnitude [dB]")
    # ax.set_xlim(-Fs/2, Fs/2)
    # ax.set_ylim(-60, 60)
    ax.grid(True)
    plt.pause(0.01) # pause briefly to show the plot
    
# close the SDR
sdr.close()
