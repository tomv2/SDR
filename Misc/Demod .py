from rtlsdr import *
from pylab import *

sdr = RtlSdr()

sdr.sample_rate = 3.2e6
sdr.center_freq = 95e6
sdr.gain = 5

samples = sdr.read_samples(256*1024)

samples = 0.5 * np.angle(samples[0:-1] * np.conj(samples[1:])) #Demod 1

samples = np.diff(np.unwrap(np.angle(samples))) #Demod 2

plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

sdr.close()

plt.xlabel('Freq')
plt.ylabel('dB')
plt.show()


