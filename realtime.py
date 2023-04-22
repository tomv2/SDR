import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
from collections import deque

# Set up the SDR device
sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 3.2e6
sdr.center_freq = 100e6
sdr.gain = 'auto'

# Set up the real-time plot
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(sdr.center_freq/1e6 - 1, sdr.center_freq/1e6 + 1)
ax.set_ylim(-120, 20)
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Power (dB)')

# Set up the circular buffer
buffer_size = 1024
sample_buffer = deque(maxlen=buffer_size)

# Define a function to update the plot
def update_plot():
    # Concatenate the most recent samples from the buffer
    samples = np.concatenate(list(sample_buffer))
    
    # Compute the power spectrum density
    PSD = np.abs(np.fft.fft(samples))**2 / (len(samples)*sdr.sample_rate)
    PSD_log = 10*np.log10(PSD)
    PSD_shifted = np.fft.fftshift(PSD_log)
    
    # Compute the frequency axis
    freq_axis = np.fft.fftfreq(len(samples), 1/sdr.sample_rate)
    freq_axis = np.fft.fftshift(freq_axis)
    freq_axis = freq_axis + sdr.center_freq
    
    # Update the plot with the new data
    line.set_data(freq_axis/1e6, PSD_shifted)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

# Start the SDR device and the real-time plot
for i in range(1000):
    samples = sdr.read_samples(buffer_size)
    sample_buffer.append(samples)
    update_plot()

plt.show()

# Close the SDR device when the plot is closed
sdr.close()
