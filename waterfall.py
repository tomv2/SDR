import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import threading

# Set up the SDR device
sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 3.2e6
sdr.center_freq = 100e6
sdr.gain = 'auto'

# Set up the circular buffer
buffer_size = 1024
sample_buffer = np.zeros(buffer_size, dtype=np.complex64)
buffer_lock = threading.Lock()

# Define a function to read samples from the SDR device and update the buffer
def read_samples():
    global sample_buffer
    while True:
        with buffer_lock:
            samples = sdr.read_samples(buffer_size)
            sample_buffer[:-buffer_size] = sample_buffer[buffer_size:]
            sample_buffer[-buffer_size:] = samples

# Define a function to update the waterfall plot
def update_plot():
    while True:
        with buffer_lock:
            samples = sample_buffer.copy()
        PSD = np.abs(np.fft.fft(samples))**2 / (len(samples)*sdr.sample_rate)
        PSD_log = 10*np.log10(PSD)
        PSD_shifted = np.fft.fftshift(PSD_log)
        freq_axis = np.fft.fftfreq(len(samples), 1/sdr.sample_rate)
        freq_axis = np.fft.fftshift(freq_axis)
        freq_axis = freq_axis + sdr.center_freq
        if freq_axis.size == PSD_shifted.size:
            plt.clf()
            plt.imshow(np.array([PSD_shifted]), aspect='auto', cmap='jet', extent=(freq_axis[0], freq_axis[-1], 0, 1))
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Time')
            plt.colorbar()
            plt.pause(0.01)

# Start the SDR device and the real-time plot
t1 = threading.Thread(target=read_samples)
t2 = threading.Thread(target=update_plot)
t1.start()
t2.start()

plt.show()

# Close the SDR device when the plot is closed
sdr.close()
