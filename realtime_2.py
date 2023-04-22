import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import threading
import time

# Function to read samples and update the plot
def update_plot(samples, sdr, ax):
    Fs = sdr.get_sample_rate()
    N = len(samples)
    PSD = np.abs(np.fft.fft(samples))**2 / (N*Fs)
    PSD_log = 10*np.log10(PSD)
    PSD_shifted = np.fft.fftshift(PSD_log)
    freq_axis = np.fft.fftfreq(len(samples), 1/Fs)
    freq_axis = np.fft.fftshift(freq_axis)
    center_frequency = sdr.get_center_freq()
    freq_axis = freq_axis + center_frequency
    f = freq_axis/1e6

    ax.clear()
    ax.plot(f, PSD_shifted)
    ax.set_xlabel("Frequency MHz")
    ax.set_ylabel("Power dB")
    ax.set_title(f"SDR Spectrum at {center_frequency/1e6:.3f} MHz")
    ax.grid(True)
    plt.draw()
    plt.pause(0.001)

# Function to continuously read samples from the SDR
def read_samples(sdr, ax):
    while True:
        try:
            samples = sdr.read_samples(256*1024)
            update_plot(samples, sdr, ax)
        except usb.core.USBError:
            print('SDR device error: USB transfer failed')
            time.sleep(1)
        except Exception as e:
            print(f'Error: {e}')
            break

# Set up the SDR device
sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 100e6
sdr.gain = 50

# Create a plot to display the spectrum
fig, ax = plt.subplots()
ax.set_ylim(-100, 0)

# Start a separate thread to read the samples and update the plot
t = threading.Thread(target=read_samples, args=(sdr, ax))
t.daemon = True
t.start()

# Show the plot
plt.show()

# Clean up the SDR device
sdr.close()
