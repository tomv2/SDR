from rtlsdr import RtlSdr
import matplotlib.pyplot as plt
import numpy as np

sdr = RtlSdr()

print("-------------------------------")
print("------Spectrum plotter V1------")
print("-------------------------------")

def main():
    global start_freq
    global stop_freq
    global center_freqin
    start_freq = float(input("Enter the start frequency: "))
    print("-------------------------------")
    stop_freq = float(input("Enter the stop frequency: "))
    print("-------------------------------")
    center_freqin = float(input("Enter the center frequency: "))
    print("-------------------------------")
    restart()

def restart():
    error = 0
    if(start_freq > stop_freq):
        print("The start frequency is greater than the stop frequency...")
        error = 1
    if(center_freqin < start_freq):
        print("The center frequency is less than the start frequency...")
        error = 1
    if(center_freqin > stop_freq):
        print("The center frequency is greater than the stop frequency...")
        error = 1
    if(error == 1):
        print("Enter 1 to re-enter values or 2 to exit")
        again = int(input())
        if(again == 1):
            main()
        elif(again == 2):
            exit()
        else:
            exit()

main()

sdr.sample_rate = 2.4e6
#sdr.freq_correction = 60
sdr.gain = 'auto'

for i in range(start_freq,stop_freq,2):
    sdr.center_freq = i*center_freqin
    samples = sdr.read_samples(256*1024)
    plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

sdr.close()

plt.xlabel('Freq')
plt.ylabel('dB')
plt.show()
