import threading
import numpy as np
import matplotlib.pyplot as plt
import rtlsdr

class RealtimePlot:
    def __init__(self):
        self.sdr = rtlsdr.RtlSdr()
        self.sdr.sample_rate = 2.4e6
        self.sdr.center_freq = 100e6
        self.sdr.gain = 'auto'

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Frequency (MHz)')
        self.ax.set_ylabel('Power (dB)')
        self.ax.set_ylim(-100, 0)
        self.ax.set_xlim(80, 120)
        self.line, = self.ax.plot([], [])

        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        self.sdr.read_samples_async(self.update_plot, int(2.4e6/8))
        self.thread.start()

    def update_plot(self, samples, *args):
        PSD = np.abs(np.fft.fft(samples))**2 / len(samples)
        PSD_log = 10*np.log10(PSD)
        PSD_shifted = np.fft.fftshift(PSD_log)
        freq_axis = np.fft.fftfreq(len(samples), 1/self.sdr.sample_rate)
        freq_axis = np.fft.fftshift(freq_axis)
        freq_axis = freq_axis + self.sdr.center_freq
        f = freq_axis/1e6

        self.line.set_xdata(f)
        self.line.set_ydata(PSD_shifted)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update(self):
        while not self.stopped:
            try:
                self.sdr.read_samples_async(self.update_plot, int(2.4e6/8))
            except usb.core.USBError:
                print("USB Error")

    def stop(self):
        self.stopped = True
        self.thread.join()
        self.sdr.cancel_read_async()
        self.sdr.close()
        rtlsdr.libusb_exit(None)

if __name__ == '__main__':
    rp = RealtimePlot()
    rp.start()
    input("Press Enter to stop...")
    rp.stop()
