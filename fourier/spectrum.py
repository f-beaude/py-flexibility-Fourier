# Fourier frequency spectrum

import numpy as np
import matplotlib.pyplot as plt

from .data import data

class spectrum:
    """ Generate the frequency spectrum from an input signal
    
    Args:
        input_signal: the signal for which to carry out the Fourier transform
        T: the time period between each signal point (in seconds)
        threshold: the threshold below which frequency components are ignored
    
    """
    # returns a dictionary (key = frequency, value = amplitude of the Fourier transform)
    def frequency(input_signal: list, T: float) -> dict:
        if (data.has_invalid_values(input_signal)):
            raise ValueError('Invalid values in the input signal: ' + str(data.invalid_values(input_signal)))
        
        N: int = len(input_signal)  # Number of sample points
        # rescale the FFT: 
        #  - *2 so that the abs of sin = 1, and
        #  - /N so that the abs is independent from the number of data points
        fft_result = np.fft.rfft(input_signal) * 2.0 / N
        frequencies_Hz = np.fft.rfftfreq(N, T)  # Frequency bins
        amplitudes = np.abs(fft_result)
    
        return dict(zip(frequencies_Hz, amplitudes))
    
    """ Filter out the zero components of a specturm
    
    Args:
        spectrum: a dictionary with keys being frequencies
        threshold: the threshold below which frequency components are ignored
    
    """
    __NON_ZERO_THRESHOLD: float = 0.01
    def filter_non_zero_components(spectrum: dict, threshold: float = __NON_ZERO_THRESHOLD) -> dict:
        return {key: value for key, value in spectrum.items() if value >= threshold}
        
    
    """ Sort the frequency spectrum according to the decreasing frequency component
    
    Args:
        spectrum: a dictionary with keys being frequencies
    """
    def resonant_frequencies(spectr: dict, threshold: float = __NON_ZERO_THRESHOLD) -> dict:
        return {key: value for key, value in sorted(spectrum.filter_non_zero_components(spectr, threshold).items(), key=lambda item: item[1], reverse = True)}
    
    
    class convert:
        """ Converts frequencies into "per day" (instead of Hz, per s)
        
        Args:
            spectrum: a dictionary with keys being frequencies in Hz
        """
        def to_per_day(spectr: dict) -> dict:
            return spectrum.convert.__to_value(spectr, 24 * 3600)
        
        """ Converts frequencies into "per month" (instead of Hz, per s)
        Month = 30.437 days (given that the number of days per month varies)
        
        Args:
            spectrum: a dictionary with keys being frequencies in Hz
        """
        def to_per_month(spectr: dict) -> dict:
            return spectrum.convert.__to_value(spectr, 30.437 * 24 * 3600)
            
        
        """ Converts frequencies into another scale (based on a coefficient)
        Month = 30.437 days (given that the number of days per month varies)
        
        Args:
            spectrum: a dictionary with keys being frequencies in Hz
            coeff: the frequency conversion coefficient
        """
        def __to_value(spectrum: dict, coeff: float) -> dict:
            return {coeff * key: value for key, value in spectrum.items()}
    
    """ Plot a given frequency spectrum
    
    Args:
        spectrum: a dictionary with keys being frequencies
        frequency_unit: the unit of frequencies (e.g. 'in days') for display purposes
    """
    def plot(spectrum:dict, frequency_unit: str):
        # Plot the frequency spectrum
        plt.figure(figsize = (12, 6))
        plt.plot(spectrum.keys(), spectrum.values())
        plt.title('Frequency Spectrum')
        plt.xlabel('Frequency (' + frequency_unit +')')
        plt.ylabel('Magnitude')
        plt.xscale('log')
        plt.grid()
        plt.show()