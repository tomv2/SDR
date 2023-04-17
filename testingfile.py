import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, firwin, resample_poly

# Load the samples from file
sample_rate = 2.4e6
x = np.fromfile('samples.dat', dtype=np.complex64)

# Quadrature demodulation
f_c = 100e6  # carrier frequency
t = np.arange(len(x)) / sample_rate
x_demod = x * np.exp(-2j * np.pi * f_c * t)

# Low-pass filter
taps = firwin(numtaps=101, cutoff=7.5e3, fs=sample_rate)
x_filtered = np.convolve(x_demod, taps, 'valid')

# Decimate by 10
x_decimated = x_filtered[::10]
sample_rate = sample_rate / 10

# Gardner timing recovery
T = 4  # symbol period
mu = 0.5  # gain factor
error = np.zeros_like(x_decimated)
mu_vec = np.zeros_like(x_decimated)
for i in range(2, len(x_decimated)):
    error[i] = np.imag(np.conj(x_decimated[i]) * x_decimated[i-2])
    mu_vec[i] = mu_vec[i-1] + mu * error[i] * np.abs(error[i-1] - error[i+1])
    x_decimated[i] = np.interp(i - mu_vec[i], np.arange(len(x_decimated)), x_decimated)

# Resample to 19 kHz
x_resampled = resample_poly(x_decimated, 19, int(sample_rate))
sample_rate = 19e3

# Compute the power spectral density
f, psd = welch(x_resampled, fs=sample_rate, nperseg=1024)

# Convert to dBm
psd_dbm = 10 * np.log10(psd) + 30

# Plot the spectrum
plt.figure()
plt.plot(f, psd_dbm)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (dBm/Hz)')
plt.show()
