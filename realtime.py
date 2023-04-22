import numpy as np
import matplotlib.pyplot as plt
import pyrtlsdr

sdr = pyrtlsdr.RtlSdr()

# Set the sample rate, center frequency, and gain
sdr.sample_rate = 3.2e6
sdr.center_freq = 100e6
sdr.gain = 'auto'

# Create a figure for the real-time plot
fig, ax = plt.subplots()

# Create an empty line object for the plot
line, = ax.plot([], [])

# Set the plot limits and labels
ax.set_xlim(sdr.center_freq/1e6 - 1, sdr.center_freq/1e6 + 1)
ax.set_ylim(-120, 20)
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Power (dB)')

# Define a function to update the plot with new samples
def update_plot(samples):
    # Compute the power spectrum density
    PSD = np.abs(np.fft.fft(samples))**2 / (len(samples)*sdr.sample_rate)
    PSD_log = 10*np.log10(PSD)
    PSD_shifted = np.fft.fftshift(PSD_log)
    
    # Compute the frequency axis
    freq_axis = np.fft.fftfreq(len(samples), 1/sdr.sample_rate)
    freq_axis = np.fft.fftshift(freq_axis)
    freq_axis = freq_axis + sdr.center_freq
    
    # Update the plot with the new data
    line.set_data(freq_axis/1e6, PSD_shifted)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

# Start the SDR device and the real-time plot
sdr.read_samples_async(update_plot, num_samples=8192)

plt.show()

# Close the SDR device when the plot is closed
sdr.close()
