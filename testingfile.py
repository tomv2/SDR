import rtlsdr
import numpy as np
import matplotlib.pyplot as plt

# Define the RTL SDR module settings
center_freq = 100e6    # Hz
sample_rate = 2.4e6    # Hz
gain = 40              # dB

# Create the RTL SDR object
sdr = rtlsdr.RtlSdr()

# Set the RTL SDR module parameters
sdr.sample_rate = sample_rate
sdr.center_freq = center_freq
sdr.gain = gain

# Read samples from the RTL SDR module
samples = sdr.read_samples(1024)

# Calculate the power spectral density (PSD)
psd = np.abs(np.fft.fft(samples))**2/len(samples)

# Create the frequency axis for the plot
freq_axis = np.fft.fftfreq(len(samples), 1/sample_rate)/1e6

# Plot the spectrum
plt.plot(freq_axis, psd)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Power Spectral Density')
plt.show()

# Close the RTL SDR object
sdr.close()
