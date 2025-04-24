import numpy as np
import scipy.io.wavfile as wav


def linear_interpolation(wave_table, idx):
    truncated_idx = int(np.floor(idx))
    next_idx = (truncated_idx+1) % wave_table.shape[0]
    
    next_idx_weight = idx - truncated_idx
    truncated_idx_weight = 1 - next_idx_weight
    
    return truncated_idx_weight * wave_table[truncated_idx] + next_idx_weight * wave_table[next_idx]


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
        # output[n] = wave_table[int(np.floor(idx))]
        output[n] = linear_interpolation(wave_table, idx) 
        idx += idxIncr
        idx %= wavetable_length
    gain = -20
    # /(n+1)-n/2     - this was part of the previous line when it was inside the func, which then ramps the gain up
    amplitude = 10 ** (gain/20)
    output *= amplitude
    
    
    
    wav.write('sine432hz_interp.wav', sample_rate, output.astype(np.float32))
    
    
if __name__ == "__main__":
    main()
        