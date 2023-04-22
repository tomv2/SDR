from flask import Flask, render_template, Response
import numpy as np
import matplotlib.pyplot as plt
import rtlsdr
import time

app = Flask(__name__)

sdr = rtlsdr.RtlSdr()

Fs = 3.2e6
Ts = 1/Fs
N= 256*1024
center_frequency = 100e6

sdr.sample_rate = Fs
sdr.center_frequency = center_frequency

def generate_plot():
    while True:
        samples = sdr.read_samples(N)
        PSD = np.abs(np.fft.fft(samples))**2 / (N*Fs)
        PSD_log = 10*np.log10(PSD)
        PSD_shifted = np.fft.fftshift(PSD_log)

        freq_axis = np.fft.fftfreq(len(samples), 1/Fs)
        freq_axis = np.fft.fftshift(freq_axis)
        freq_axis = freq_axis + center_frequency
        f = freq_axis/1e6

        plt.clf() # Clear previous plot
        plt.plot(f, PSD_shifted)
        plt.xlabel("Frequency Hz")
        plt.ylabel("Power dB")
        plt.grid(True)
        
        # Convert the plot to a PNG image and return it as a response
        # with a content type of image/png
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + buf.getvalue() + b'\r\n')
        buf.close()

        time.sleep(0.1) # Add a small delay to control update rate

@app.route('/')
def index():
    # Render the template that displays the plot
    return render_template('index.html')

@app.route('/plot.png')
def plot_png():
    # Return a response that streams the plot as a PNG image
    return Response(generate_plot(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
