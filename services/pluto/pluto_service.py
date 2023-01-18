import adi
import numpy as np
import redis
from matplotlib import pyplot as plt

N_THREADS = 1

def find_sdr():
    return 'usb:1.3.5'

def setup_sdr(uri: str):
    sdr = adi.Pluto(uri=uri)
    return sdr

def main():
    sdr_uri = find_sdr()
    sdr = setup_sdr(uri=sdr_uri)
    
    data = sdr.rx()
    spectrum = 10 * np.log10(abs(np.fft.fftshift(np.fft(data))))

    plt.plot(spectrum)
    plt.show()


if __name__== '__main__':
    main()