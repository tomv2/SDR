import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # set backend to Qt5
import matplotlib.pyplot as plt
import rtlsdr
import threading

# Set up the SDR device
sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 3.2e6
sdr.center_freq = 100e6
sdr.gain = 'auto'

# Set up the real-time plot
fig, ax = plt.subplots()
line = ax.imshow(np.zeros((512, 1024)), aspect='auto', cmap='viridis')
ax.set_xlabel('Time')
ax.set_ylabel('Frequency (MHz)')
fig.colorbar(line)

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

# Define a function to update the plot
def update_plot():
    while True:
        with buffer_lock:
            samples = sample_buffer.copy()
        PSD = np.abs(np.fft.fft(samples, axis=0))**2 / (len(samples)*sdr.sample_rate)
        PSD_log = 10*np.log10(PSD)
        PSD_shifted = np.fft.fftshift(PSD_log, axes=0)
        freq_axis = np.fft.fftfreq(len(samples), 1/sdr.sample_rate)
        freq_axis = np.fft.fftshift(freq_axis) + sdr.center_freq/1e6
        line.set_data(np.arange(PSD_shifted.shape[1]), freq_axis, PSD_shifted)
        fig.canvas.draw()

# Start the SDR device and the real-time plot
t1 = threading.Thread(target=read_samples)
t2 = threading.Thread(target=update_plot)
t1.start()
t2.start()

plt.show()

# Close the SDR device when the plot is closed
sdr.close()
