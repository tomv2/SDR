from rtlsdr import RtlSdr
import matplotlib.pyplot as plt
import numpy as np
from pylab import *


def update_psd():
    # create SDR instance
    sdr = RtlSdr()

    # configure device
    sdr.sample_rate = 2.4e6
    sdr.center_freq = 95e6
    sdr.gain = 4

    while True:
        try:
            # read samples
            samples = sdr.read_samples(256*1024)

            # plot PSD
            psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
            xlabel('Frequency (MHz)')
            ylabel('Relative power (dB)')
            draw()

        except KeyboardInterrupt:
            break

    # close SDR device
    sdr.close()

# initialize plot
ion()
figure()

# start updating PSD
update_psd()

# block until plot window is closed
ioff()
show()

