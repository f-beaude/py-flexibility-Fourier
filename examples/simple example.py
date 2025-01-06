import os.path
import pandas as pd
import statistics
import sys
import warnings

# import the package using path to directory
sys.path.append (os.path.join('..'))
import fourier


def main():
    
    # parameter: whether to save the resulting frequencies (None = don't save)
    path_to_output_spectrum: str = os.path.join('..', 'output', 'frequency_spectrum.csv')
    
    # extract data from a CSV file (assuming that the first row includes column names)
    # requires an example file. Data can e.g. be downloaded from ENTSO-E's transparency platform
    data_path: str = os.path.join('..', 'data', 'Load 2023.csv')
    assert os.path.isfile(data_path), "File doesn't exist: " + data_path

    csv_data_full = pd.read_csv(data_path, sep=',', header = 0)
    csv_data_column = pd.to_numeric(csv_data_full['Actual Total Load'], errors = 'raise')
    T: int = 15 * 60 # time period between two data points, in s
    
    # interpolate when finding missing values
    if fourier.data.has_invalid_values(csv_data_column):
        warnings.warn("Invalid values in data --> replaced with linear interpolation")
        csv_data_column = csv_data_column.interpolate()
    
    # remove the average of the data, to generate a centered data set (i.e. removing the 0-frequency component)
    average_data: float = statistics.fmean(csv_data_column)
    centered_data_column: list = [value - average_data for value in csv_data_column]
    
    # calculate (and plot) the frequency spectrum of the Fourier transform
    frequency_spectrum: dict = fourier.spectrum.convert.to_per_day(fourier.spectrum.frequency(centered_data_column, T))
    fourier.spectrum.plot(frequency_spectrum, "per day")
    
    # extract and export the resonant frequencies
    resonant_frequencies: dict = fourier.spectrum.resonant_frequencies(frequency_spectrum)
    if (not path_to_output_spectrum is None):
        output_data = pd.DataFrame({'frequency (per day)' : resonant_frequencies.keys(), 'amplitude':resonant_frequencies.values()})
        output_data.to_csv(path_to_output_spectrum, index = False)
    
main()
