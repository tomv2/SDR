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

# Define a function to update the plot
def update_plot():
    fig, ax = plt.subplots()
    plt.ion()
    fig.show()
    fig.canvas.draw()
    
    PSD_log_all = []
    freq_axis = None
    while True:
        with buffer_lock:
            samples = sample_buffer.copy()
        PSD = np.abs(np.fft.fft(samples))**2 / (len(samples)*sdr.sample_rate)
        PSD_log = 10*np.log10(PSD)
        PSD_log_all.append(PSD_log)
        
        # Update the frequency axis once
        if freq_axis is None:
            freq_axis = np.fft.fftfreq(len(samples), 1/sdr.sample_rate)
            freq_axis = np.fft.fftshift(freq_axis)
            freq_axis = freq_axis + sdr.center_freq
            freq_axis = np.resize(freq_axis, (len(samples)//buffer_size, buffer_size))
            freq_axis = np.fft.fftshift(freq_axis, axes=1)
            extent = [freq_axis.min()/1e6, freq_axis.max()/1e6, 0, len(PSD_log_all)]

        PSD_log_all_resized = np.array(PSD_log_all)
        if PSD_log_all_resized.shape[0] > len(samples)//buffer_size:
            PSD_log_all_resized = PSD_log_all_resized[-(len(samples)//buffer_size):, :]

        ax.imshow(PSD_log_all_resized.T, origin='lower', aspect='auto', cmap='jet', extent=extent)
        ax.set_xlabel('Frequency (MHz)')
        ax.set_ylabel('FFT Window')
        fig.canvas.draw()
        fig.canvas.flush_events()

# Start the SDR device and the real-time plot
sdr_thread = threading.Thread(target=read_samples)
sdr_thread.start()

plot_thread = threading.Thread(target=update_plot)
plot_thread.start()

plt.show()

# Close the SDR device when the plot is closed
sdr.close()
