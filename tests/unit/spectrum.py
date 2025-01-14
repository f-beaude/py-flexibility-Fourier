import matplotlib.pyplot as plt
import numpy as np
import os.path
import unittest
import sys

# import the package using path to directory
sys.path.append (os.path.join('..', '..'))
import fourier

class spectrum:
    
    def all ():
        spectrum.Spectrum().all()

    class Spectrum(unittest.TestCase):
        def all(self):
            self.__simple_transforms()
            self.__resonant_frequencies()
            self.__plot()
            self.__conversions()

        # Generate a sinusoidal wave (to test whether the computed frequencies are correct)
        def __generate_sine_wave(self, freq, sample_rate: int, duration: int):
            x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
            frequencies = x * freq
            # 2pi because np.sin takes radians
            y = np.sin((2 * np.pi) * frequencies)
            return x, y
        
        # Simple Fourier transform (to test error catching)
        def __simple_transforms(self):
            sample_rate: int = 30
            duration: int = 15
            
            T1: float = 1
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            spectrum1 = fourier.spectrum.frequency(signal1, float(1/sample_rate))
            plt.figure(figsize=(12, 6))
            plt.plot(signal1)
            plt.show()
            fourier.spectrum.plot(spectrum1, 'Hz')
            
            signal_NA = np.append(signal1, np.nan)
            with self.assertRaises(ValueError):
                 fourier.spectrum.frequency(signal_NA, float(1/sample_rate))
            signal_infinity = np.append(signal1, np.inf)
            with self.assertRaises(ValueError):
                 fourier.spectrum.frequency(signal_infinity, float(1/sample_rate))

        # Resonant frequencies
        def __resonant_frequencies(self):
            sample_rate: int = 20
            duration: int = 40
            
            T1: float = 4.0
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            spectrum1 = fourier.spectrum.frequency(signal1, float(1/sample_rate))
            resonant_frequencies1 = fourier.spectrum.resonant_frequencies(spectrum1)
            self.assertEqual(len(resonant_frequencies1), 1)
            self.assertAlmostEqual(list(resonant_frequencies1)[0], 1/T1, delta = 0.1)
            
            T2: float = 2.0
            __, signal2 = self.__generate_sine_wave(1/T2, sample_rate, duration)
            signal12 = signal1 + 0.5 * signal2
            spectrum12 = fourier.spectrum.frequency(signal12, float(1/sample_rate))
            
            resonant_frequencies12 = fourier.spectrum.resonant_frequencies(spectrum12)
            resonant_frequencies12_freqs: list = list(resonant_frequencies12.keys())
            resonant_frequencies12_abs: list = list(resonant_frequencies12.values())
            
            self.assertAlmostEqual(resonant_frequencies12_freqs[0], 1/T1, delta = 0.01)
            self.assertAlmostEqual(resonant_frequencies12_freqs[1], 1/T2, delta = 0.01)
            self.assertAlmostEqual(resonant_frequencies12_abs[0], 1.0, delta = 0.01)
            self.assertAlmostEqual(resonant_frequencies12_abs[0], 2 * resonant_frequencies12_abs[1], delta = 0.01)
        
        def __plot(self):
            sample_rate: int = 10
            duration: int = 60
            T1: float = 6.0
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            T2: float = 3.0
            __, signal2 = self.__generate_sine_wave(1/T2, sample_rate, duration)
            signal12 = signal1 + 0.5 * signal2
            
            spectrum12 = fourier.spectrum.frequency(signal12, float(1/sample_rate))
            # plot
            fourier.spectrum.plot(spectrum12, 'Hz')
        
        def __conversions(self):
            sample_rate: int = 10
            duration: int = 40
            
            T1: float = 4
            T2: float = 2
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            __, signal2 = self.__generate_sine_wave(1/T2, sample_rate, duration)
            signal12 = signal1 + 0.5 * signal2
            spectrum12 = fourier.spectrum.frequency(signal12, float(1/sample_rate))
            
            spectrum12_days: dict = fourier.spectrum.convert.to_per_day(spectrum12)
            self.assertTrue(all(x == y for x, y in zip(spectrum12.values(), spectrum12_days.values())))
            self.assertTrue(all(24 * 3600 * x == y for x, y in zip(spectrum12.keys(), spectrum12_days.keys())))
            
            spectrum12_months: dict = fourier.spectrum.convert.to_per_month(spectrum12)
            self.assertTrue(all(x == y for x, y in zip(spectrum12.values(), spectrum12_months.values())))
            self.assertTrue(all(30.437 * 24 * 3600 * x == y for x, y in zip(spectrum12.keys(), spectrum12_months.keys())))

def main():
    spectrum.all()
#main()
