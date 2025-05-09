import numpy as np
import scipy.io.wavfile as wav
import pandas as pd


def linear_interpolation(wave_table, idx):
    truncated_idx = int(np.floor(idx))
    next_idx = (truncated_idx+1) % wave_table.shape[0]
    
    next_idx_weight = idx - truncated_idx
    truncated_idx_weight = 1 - next_idx_weight
    
    return truncated_idx_weight * wave_table[truncated_idx] + next_idx_weight * wave_table[next_idx]

def fade(signal, fade_length=1000):
    fade_in = (1-np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)
    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length:])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])
    
    return signal


def saw_tooth(x):
    return (x + np.pi) / np.pi % 2 -1
        

def main():
    sample_rate = 44100
    f = 216
    t = 3
    waveform = saw_tooth
    
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
    
    output = fade(output)
    
    
    
    wav.write('saw216hz.wav', sample_rate, output.astype(np.float32))
    
    
if __name__ == "__main__":
    main()
        