import time
import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import usb.core
import usb.util

sdr = rtlsdr.RtlSdr()
Fs = 3.2e6
Ts = 1/Fs
N = 256*1024
center_frequency = 100e6

sdr.sample_rate = Fs
sdr.center_frequency = center_frequency

try:
    while True:
        samples = sdr.read_samples(N)
        PSD = np.abs(np.fft.fft(samples))**2 / (N*Fs)
        PSD_log = 10*np.log10(PSD)
        PSD_shifted = np.fft.fftshift(PSD_log)

        freq_axis = np.fft.fftfreq(len(samples), 1/Fs)
        freq_axis = np.fft.fftshift(freq_axis)
        freq_axis = freq_axis + center_frequency
        f = freq_axis/1e6

        plt.clf()  # clear the previous plot
        plt.plot(f, PSD_shifted)
        plt.xlabel("Frequency Hz")
        plt.ylabel("Power dB")
        plt.grid(True)
        plt.pause(0.01)  # pause to allow plot to update

except usb.core.USBError as e:
    print(f"USB error: {e}")

finally:
    sdr.close()
