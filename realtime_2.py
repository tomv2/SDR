import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import usb.core
import usb.util

class SDRThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.sdr = rtlsdr.RtlSdr()
        self.Fs = 3.2e6
        self.Ts = 1/self.Fs
        self.N = 256*1024
        self.center_frequency = 100e6
        self.sdr.sample_rate = self.Fs
        self.sdr.center_frequency = self.center_frequency

    def run(self):
        try:
            while True:
                samples = self.sdr.read_samples(self.N)
                PSD = np.abs(np.fft.fft(samples))**2 / (self.N*self.Fs)
                PSD_log = 10*np.log10(PSD)
                PSD_shifted = np.fft.fftshift(PSD_log)

                freq_axis = np.fft.fftfreq(len(samples), 1/self.Fs)
                freq_axis = np.fft.fftshift(freq_axis)
                freq_axis = freq_axis + self.center_frequency
                f = freq_axis/1e6

                plt.clf()  # clear the previous plot
                plt.plot(f, PSD_shifted)
                plt.xlabel("Frequency Hz")
                plt.ylabel("Power dB")
                plt.grid(True)
                plt.pause(0.01)  # pause to allow plot to update

        except usb.core.USBError as e:
            print(f"USB error: {e}")

        finally:
            self.sdr.close()

if __name__ == "__main__":
    try:
        thread = SDRThread()
        thread.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        thread.sdr.cancel_read_async()
        thread.sdr.close()
