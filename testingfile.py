import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import decimate, firwin, resample_poly
from rtlsdr import RtlSdr

# Setup the RTL-SDR device
sdr = RtlSdr()

# Set the sample rate and center frequency
sample_rate = 2.4e6
center_freq = 100e6
sdr.sample_rate = sample_rate
sdr.center_freq = center_freq

# Read samples from the RTL-SDR
samples = sdr.read_samples(256*1024)

# Freq shift
N = len(samples)
f_o = -1e6 # amount we need to shift by
t = np.arange(N)/sample_rate # time vector
samples = samples * np.exp(2j*np.pi*f_o*t) # down shift

# Low-Pass Filter
taps = firwin(numtaps=101, cutoff=0.5e6, fs=sample_rate)
samples = np.convolve(samples, taps, 'valid')

# Decimate by 10, now that we filtered and there won't be aliasing
samples = decimate(samples, 10)

# Resample to 19 kHz
samples = resample_poly(samples, 19e3, sample_rate)

# Compute the spectrum
frequencies, spectrum = plt.psd(samples, NFFT=1024, Fs=19e3, scale_by_freq=True, window=np.blackman(1024))

# Convert the spectrum to dBm
spectrum_dbm = 10 * np.log10(spectrum + 1e-12) + 30


# Plot the spectrum
plt.plot(frequencies/1e6, spectrum_dbm)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Power Spectral Density (dBm/Hz)')
plt.show()

# Close the RTL-SDR device
sdr.close()
