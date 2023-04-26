import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import threading

# Set up the SDR device
sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 3.2e6
sdr.center_freq = 100e6
sdr.gain = 'auto'

# Set up the waterfall plot
fig, ax = plt.subplots()
waterfall = np.zeros((1024, 1000))
im = ax.imshow(waterfall, extent=[sdr.center_freq/1e6 - 1, sdr.center_freq/1e6 + 1, 0, 1024], aspect='auto', cmap='jet')
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Time')

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
    global waterfall
    while True:
        with buffer_lock:
            samples = sample_buffer.copy()
            PSD = np.abs(np.fft.fft(samples))**2 / (len(samples)*sdr.sample_rate)
            PSD_log = 10*np.log10(PSD)
            PSD_shifted = np.fft.fftshift(PSD_log)
            waterfall[:-1] = waterfall[1:]
            waterfall[-1] = PSD_shifted
            im.set_data(waterfall)
            fig.canvas.draw()

# Start the SDR device and the real-time plot
t1 = threading.Thread(target=read_samples)
t2 = threading.Thread(target=update_plot)
t1.start()
t2.start()

plt.show()

# Close the SDR device when the plot is closed
sdr.close()
