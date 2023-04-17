import numpy as np
from scipy import signal
from rtlsdr import RtlSdr

# Set RTL-SDR parameters
freq = 100e6
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = freq
sdr.gain = 20

# Collect samples
samples = sdr.read_samples(256*1024)

# Freq shift
N = len(samples)
f_o = -57e3 # amount we need to shift by
t = np.arange(N)/sdr.sample_rate # time vector
samples = samples * np.exp(2j*np.pi*f_o*t) # down shift

# Low-Pass Filter
taps = signal.firwin(numtaps=101, cutoff=7500, fs=sdr.sample_rate)
samples = np.convolve(samples, taps, 'valid')

# Decimate by 10, now that we filtered and there won't be aliasing
samples = samples[::10]
sdr.sample_rate /= 10

# Resample to 19kHz
samples = signal.resample_poly(samples, 19*sdr.sample_rate, sdr.sample_rate)
sdr.sample_rate = 19*sdr.sample_rate

# Perform quadrature demodulation
I = np.real(samples)
Q = np.imag(samples)
samples = I[:-1]*Q[1:] - I[1:]*Q[:-1]

# Perform symbol synchronization
samples = samples[1500:-1500]
samples = samples-np.mean(samples)
samples = np.sign(samples)

# Calculate spectrum
f, Pxx = signal.welch(x=samples, fs=sdr.sample_rate, nperseg=1024)

# Convert power to dBm
Pxx = 10*np.log10(Pxx/1e-3)

# Plot spectrum
import matplotlib.pyplot as plt
plt.plot(f/1e6, Pxx)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Power Spectral Density (dBm/Hz)')
plt.show()
