import matplotlib.pyplot as plt
import matplotlib.pyplot as plts
from rtlsdr import *

sdr = RtlSdr()

ppm = sdr.get_freq_correction()
print 'Frequency correction ' + str(ppm)
tuner_type = sdr.get_tuner_type()
print 'Tuner type ' + str(tuner_type)

sdr.sample_rate = 2.4e6
sdr.center_freq = 392.0125e6
sdr.gain = 7

plts.title('Power spectral density')
plts.xlabel('Frequency (MHz)')
plts.ylabel('Relative power (dB)')
plts.grid(True)
lines, = plts.plot(0, 0)
plts.ion()
fig = plts.figure()

while True:
    samples = sdr.read_samples(256*1024)
    plt.psd(samples, NFFT=512, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    line = plt.gca().lines[0]
    lines.set_xdata(line.get_xdata())
    lines.set_ydata(line.get_ydata())
    fig.canvas.draw()
