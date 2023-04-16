from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import time

sdr = RtlSdr()

sdr.sample_rate = 2.4e6
sdr.freq_correction = 60
sdr.gain = 1

Fs = 2.4e6 # sample rate
Ts = 1/Fs # sample period
N = 256*1024 # number of samples 

# create the figure and axis for the plot
fig, ax = plt.subplots()
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("Magnitude [dB]")
ax.set_xlim(-Fs/2, Fs/2)
ax.set_ylim(-60, 60)
ax.grid(True)

while True:
    x = psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

    f = np.arange(-Fs/2, Fs/2, Fs/N) # start, stop, step

    # update the data for the plot
    ax.clear()
    ax.plot(f, x)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Magnitude [dB]")
    ax.set_xlim(-Fs/2, Fs/2)
    ax.set_ylim(-60, 60)
    ax.grid(True)
    plt.pause(0.1) # pause for 1 second to show the plot
