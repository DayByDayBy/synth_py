import numpy as np
import scipy.io.wavfile as wav

def main():
    sample_rate = 44100
    f = 432
    t = 3
    waveform = np.sin
    
    wavetable_length = 64
    wave_table = np.zeros((wavetable_length,))
    
    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)
    
    output = np.zeros((t * sample_rate,))
    
    idx = 0
    idxIncr = f * wavetable_length/sample_rate
    
    for n in range(output.shape[0]):
        output[n] = wave_table[int(np.floor(idx))]
        idx += (idxIncr+34)/300
        idx %= wavetable_length
    
    wav.write('al_sine432hz.wav', sample_rate, output.astype(np.float32))
    
    
if __name__ == "__main__":
    main()
        