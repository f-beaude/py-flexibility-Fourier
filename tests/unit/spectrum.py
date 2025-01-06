import numpy as np
import os.path
import pandas as pd
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
            sample_rate: int = 1000
            duration: int = 10000
            
            T1 = 1 / 400
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            spectrum1 = fourier.spectrum.frequency(signal1, float(1/sample_rate))
            
            signal_NA = np.append(signal1, np.nan)
            with self.assertRaises(ValueError):
                 fourier.spectrum.frequency(signal_NA, float(1/sample_rate))
            signal_infinity = np.append(signal1, np.inf)
            with self.assertRaises(ValueError):
                 fourier.spectrum.frequency(signal_infinity, float(1/sample_rate))

        # Resonant frequencies
        def __resonant_frequencies(self):
            sample_rate: int = 1000
            duration: int = 10000
            
            T1 = 1 / 400
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            spectrum1 = fourier.spectrum.frequency(signal1, float(1/sample_rate))
            resonant_frequencies1 = fourier.spectrum.resonant_frequencies(spectrum1)
            self.assertEqual(len(resonant_frequencies1), 1)
            self.assertAlmostEqual(list(resonant_frequencies1)[0], 1/T1, delta = 0.1)
            
            T2 = 1/200
            __, signal2 = self.__generate_sine_wave(1/T2, sample_rate, duration)
            signal12 = signal1 + 0.5 * signal2
            spectrum12 = fourier.spectrum.frequency(signal12, float(1/sample_rate))
            
            resonant_frequencies12 = fourier.spectrum.resonant_frequencies(spectrum12)
            resonant_frequencies12_freqs = list(resonant_frequencies12.keys())
            resonant_frequencies12_abs = list(resonant_frequencies12.values())
            
            self.assertAlmostEqual(resonant_frequencies12_freqs[0], 1/T1, delta = 0.1)
            self.assertAlmostEqual(resonant_frequencies12_freqs[1], 1/T2, delta = 0.1)
            self.assertAlmostEqual(resonant_frequencies12_abs[0], 2 * resonant_frequencies12_abs[1], delta = 0.1)
        
        def __plot(self):
            sample_rate: int = 1000
            duration: int = 10000
            T1 = 1 / 400
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            T2 = 1/200
            __, signal2 = self.__generate_sine_wave(1/T2, sample_rate, duration)
            signal12 = signal1 + 0.5 * signal2
            
            spectrum12 = fourier.spectrum.frequency(signal12, float(1/sample_rate))
            # plot
            fourier.spectrum.plot(spectrum12, 'Hz')
        
        def __conversions(self):
            sample_rate: int = 1000
            duration: int = 10000
            
            T1 = 1 / 400
            T2 = 1/200
            __, signal1 = self.__generate_sine_wave(1/T1, sample_rate, duration)
            __, signal2 = self.__generate_sine_wave(1/T2, sample_rate, duration)
            signal12 = signal1 + 0.5 * signal2
            spectrum12 = fourier.spectrum.frequency(signal12, float(1/sample_rate))
            
            spectrum12_days = fourier.spectrum.convert.to_per_day(spectrum12)
            self.assertTrue(all(x == y for x, y in zip(spectrum12.values(), spectrum12_days.values())))
            self.assertTrue(all(24 * 3600 * x == y for x, y in zip(spectrum12.keys(), spectrum12_days.keys())))
            
            spectrum12_months = fourier.spectrum.convert.to_per_month(spectrum12)
            self.assertTrue(all(x == y for x, y in zip(spectrum12.values(), spectrum12_months.values())))
            self.assertTrue(all(30.437 * 24 * 3600 * x == y for x, y in zip(spectrum12.keys(), spectrum12_months.keys())))
            

###
            # self.assertEqual(myCountry.name_is_set(), False)
            # self.assertEqual(myCountry.get_name(), None)
            # myCountry.set_name('Banana Republic')
            # self.assertEqual(myCountry.name_is_set(), True)
            # self.assertEqual(myCountry.get_name(), 'Banana Republic')

            # self.assertEqual(myCountry.ucte_letter_is_set(), False)
            # self.assertEqual(myCountry.get_ucte_letter(), None)
            # myCountry.set_ucte_letter('Z')
            # self.assertEqual(myCountry.ucte_letter_is_set(), True)
            # self.assertEqual(myCountry.get_ucte_letter(), 'Z')
            # with self.assertRaises(ValueError):
            #     myCountry.set_ucte_letter('ZZ')

            # self.assertEqual(myCountry.iso2_is_set(), False)
            # self.assertEqual(myCountry.get_iso2(), None)
            # myCountry.set_iso2('BR')
            # self.assertEqual(myCountry.iso2_is_set(), True)
            # self.assertEqual(myCountry.get_iso2(), 'BR')
            # with self.assertRaises(ValueError):
            #     myCountry.set_iso2('A')
            # with self.assertRaises(ValueError):
            #     myCountry.set_iso2('ABC')

            # # check that nothing was unintentionally written in the meantime
            # self.assertEqual(myCountry.get_name(), 'Banana Republic')
            # self.assertEqual(myCountry.get_ucte_letter(), 'Z')
            # self.assertEqual(myCountry.get_iso2(), 'BR')

def main():
    spectrum.all()
#main()