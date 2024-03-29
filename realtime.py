import rtlsdr
import numpy as np
import matplotlib.pyplot as plt
import threading

sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 100e6
sdr.gain = 1

fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(sdr.center_freq/1e6 - 1, sdr.center_freq/1e6 + 1)
ax.set_ylim(-120, 20)
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Power (dB)')

buffer_size = 1024
sample_buffer = np.zeros(buffer_size, dtype=np.complex64)
buffer_lock = threading.Lock()

def read_samples():
    global sample_buffer
    while True:
        with buffer_lock:
            samples = sdr.read_samples(buffer_size)
            sample_buffer[:-buffer_size] = sample_buffer[buffer_size:]
            sample_buffer[-buffer_size:] = samples

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
        line.set_data(freq_axis/1e6, PSD_shifted)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()

t1 = threading.Thread(target=read_samples)
t2 = threading.Thread(target=update_plot)
t1.start()
t2.start()

plt.show()

sdr.close()
