from __future__ import division
import matplotlib.animation as animation
from matplotlib.mlab import psd
import pylab as pyl
import numpy as np
import sys
from rtlsdr import RtlSdr

# A simple waterfall, spectrum plotter
#
# Controls:
#
# * Scroll mouse-wheel up or down, or press the left or right arrow keys, to
#   change the center frequency (hold shift for finer control).
# * Press "+" and "-" to control gain, and space to enable AGC.
# * Type a frequency (in MHz) and press enter to directly change the center frequency

NFFT = 1024*4
NUM_SAMPLES_PER_SCAN = NFFT*16
NUM_BUFFERED_SWEEPS = 100

# change this to control the number of scans that are combined in a single sweep
# (e.g. 2, 3, 4, etc.) Note that it can slow things down
NUM_SCANS_PER_SWEEP = 1

# these are the increments when scrolling the mouse wheel or pressing '+' or '-'
FREQ_INC_COARSE = 1e6
FREQ_INC_FINE = 0.1e6
GAIN_INC = 5

class Waterfall(object):
    keyboard_buffer = []
    shift_key_down = False
    image_buffer = -100*np.ones((NUM_BUFFERED_SWEEPS,\
                                 NUM_SCANS_PER_SWEEP*NFFT))

    def __init__(self, sdr=None, fig=None):
        self.fig = fig if fig else pyl.figure()
        self.sdr = sdr if sdr else RtlSdr()

        self.init_plot()

    def init_plot(self):
        self.ax = self.fig.add_subplot(1,1,1)
        self.image = self.ax.imshow(self.image_buffer, aspect='auto',\
                                    interpolation='nearest', vmin=-50, vmax=10)
        self.ax.set_xlabel('Current frequency (MHz)')
        self.ax.get_yaxis().set_visible(False)
        self.colorbar = self.set_colorbar()

        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)

    def set_colorbar(self):
        """Sets a color bar for the plot."""
        colorbar = self.fig.colorbar(self.image)
        colorbar.set_label('Power (dB)')
        return colorbar

    def set_center_freq(self, freq):
        """Sets center frequency based on user input."""
        center_freq = float(freq)*1e6
        self.sdr.fc = center_freq
        self.update_plot_labels()

    def update_plot_labels(self):
        fc = self.sdr.fc
        rs = self.sdr.rs
        freq_range = (fc - rs/2)/1e6, (fc + rs*(NUM_SCANS_PER_SWEEP - 0.5))/1e6

        self.image.set_extent(freq_range + (0, 1))
        self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        if event.button == 'up':
            self.sdr.fc += FREQ_INC_FINE if self.shift_key_down else FREQ_INC_COARSE
            self.update_plot_labels()
        elif event.button == 'down':
            self.sdr.fc -= FREQ_INC_FINE if self.shift_key_down else F
