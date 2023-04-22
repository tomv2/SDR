import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import threading
import queue
import usb.core
import usb.util

class SDR:
    def __init__(self, center_frequency, sample_rate):
        self.center_frequency = center_frequency
        self.sample_rate = sample_rate
        self.sdr = rtlsdr.RtlSdr()

        self.sdr.sample_rate = self.sample_rate
        self.sdr.center_frequency = self.center_frequency

    def get_samples(self, N):
        try:
            samples = self.sdr.read_samples(N)
            return samples
        except usb.core.USBError:
            usb.util.dispose_resources(self.sdr.dev)
            self.sdr = rtlsdr.RtlSdr()
            self.sdr.sample_rate = self.sample_rate
            self.sdr.center_frequency = self.center_frequency
            return None

class Plotter:
    def __init__(self, queue):
        self.queue = queue
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("Frequency Hz")
        self.ax.set_ylabel("Power dB")
        self.ax.grid(True)

    def start(self):
        self.thread = threading.Thread(target=self._plot_thread)
        self.thread.daemon = True
        self.thread.start()

    def _plot_thread(self):
        while True:
            try:
                samples, freq_axis = self.queue.get()
                PSD = np.abs(np.fft.fft(samples))**2 / (len(samples)*Fs)
                PSD_log = 10*np.log10(PSD)
                PSD_shifted = np.fft.fftshift(PSD_log)
                f = freq_axis/1e6

                self.ax.clear()
                self.ax.plot(f, PSD_shifted)
                plt.pause(0.01)

            except Exception as e:
                print(e)

if __name__ == '__main__':
    Fs = 3.2e6
    Ts = 1/Fs
    N = 256 * 1024
    center_frequency = 100e6

    sdr = SDR(center_frequency, Fs)
    plot_queue = queue.Queue()
    plot = Plotter(plot_queue)
    plot.start()

    while True:
        samples = sdr.get_samples(N)
        if samples is not None:
            freq_axis = np.fft.fftfreq(len(samples), Ts)
            freq_axis = np.fft.fftshift(freq_axis)
            freq_axis = freq_axis + center_frequency

            plot_queue.put((samples, freq_axis))
