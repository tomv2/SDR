from rtlsdr import *
from pylab import *

sdr = RtlSdr()

sdr.sample_rate = 3.2e6
sdr.center_freq = 100e6
sdr.gain = 5

samples = sdr.read_samples(500e3)

psd(samples, NFFT=1024, Fs=sdr.rs/1e6, Fc=sdr.fc/1e6)   
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

show()
