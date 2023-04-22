import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import threading
import usb.core
import usb.util


class SDRThread(threading.Thread):
    def __init__(self, sdr, Fs, N, center_frequency):
        threading.Thread.__init__(self)
        self.sdr = sdr
        self.Fs = Fs
        self.Ts = 1/Fs
        self.N = N
        self.center_frequency = center_frequency
        self.running = True
        self.daemon = True

    def run(self):
        while self.running:
            try:
                samples = self.sdr.read_samples(self.N)
            except usb.core.USBError:
                # USB error occurred, try to re-attach the device
                self.sdr.close()
                self.sdr = rtlsdr.RtlSdr()
                self.sdr.sample_rate = self.Fs
                self.sdr.center_frequency = self.center_frequency
                continue

            PSD = np.abs(np.fft.fft(samples))**2 / (self.N*self.Fs)
            PSD_log = 10*np.log10(PSD)
            PSD_shifted = np.fft.fftshift(PSD_log)

            freq_axis = np.fft.fftfreq(len(samples), 1/self.Fs)
            freq_axis = np.fft.fftshift(freq_axis)
            freq_axis = freq_axis + self.center_frequency
            f = freq_axis/1e6

            plt.clf()
            plt.plot(f, PSD_shifted)
            plt.xlabel("Frequency Hz")
            plt.ylabel("Power dB")
            plt.grid(True)
            plt.pause(0.001)

        self.sdr.close()

    def stop(self):
        self.running = False


sdr = rtlsdr.RtlSdr()

Fs = 3.2e6
Ts = 1/Fs
N = 256*1024
center_frequency = 100e6

sdr.sample_rate = Fs
sdr.center_frequency = center_frequency

# Call set_wakeup_fd in the main thread
plt.ion()
plt.plot([0], [0])
plt.show(block=False)
plt.pause(0.001)
mgr = plt.get_current_fig_manager()
mgr.window.showMaximized()
usb.util.dispose_resources()
usb.util.release_interface(sdr.dev, sdr.interface)
usb.util.dispose_resources(sdr.dev)
usb.util.claim_interface(sdr.dev, sdr.interface)
usb.util.dispose_resources(sdr.dev)
usb.util.claim_interface(sdr.dev, sdr.interface)
plt.draw()
plt.pause(0.001)

sdr_thread = SDRThread(sdr, Fs, N, center_frequency)
sdr_thread.start()

input("Press Enter to stop...")
sdr_thread.stop()
sdr_thread.join()
