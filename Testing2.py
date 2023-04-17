from rtlsdr import RtlSdr
import matplotlib.pyplot as plt
import numpy as np

sdr = RtlSdr()

sdr.sample_rate = 2.4e6
sdr.freq_correction = 60
sdr.gain = 'auto'

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
lines = ax.plot([], [])
ax.set_xlabel('Freq')
ax.set_ylabel('dB')
ax.set_title('Spectrum')

while True:
    for i in range(90, 110, 2):
        sdr.center_freq = i*1e6
        samples = sdr.read_samples(256*1024)
        freqs, psd = plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
        lines[0].set_data(freqs, psd)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()

