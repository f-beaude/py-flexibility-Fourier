import datetime
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
    
    ## Two ways of importing data
    # 1. Extract data from a CSV file (assuming that the first row includes column names)
    # requires an example file. Data can e.g. be downloaded from ENTSO-E's transparency platform
    input_data_path: str = os.path.join('..', 'data', '2024 ES generation.csv')
    data_column = fourier.data.csv.read (file_path = input_data_path, column_name = 'Solar - Actual Aggregated [MW]')

    # 2. Running an SQL query
    sql_query: str = "SELECT * FROM my_table"
    data_column_raw = fourier.data.db.query(sql_query)
    data_column = fourier.data.db.extract_data_from_query_results(data_column_raw, "date_time", "load", datetime.timedelta(hours = 1))
    
    #T: int = 15 * 60 # time period between two data points, in s
    T: int = 60 * 60 # time period between two data points, in s
    
    # interpolate when finding missing values
    if fourier.data.has_invalid_values(data_column):
        warnings.warn("Replaced " + str(len(fourier.data.invalid_values(data_column))) + " missing values with linear interpolation")
        data_column = data_column.interpolate()
    
    # remove the average of the data, to generate a centered data set (i.e. removing the 0-frequency component)
    average_data: float = statistics.fmean(data_column)
    centered_data_column: list = [value - average_data for value in data_column]
    assert abs(statistics.fmean(centered_data_column)) < 0.1, "Centered data is not centered"
    
    # calculate (and plot) the frequency spectrum of the Fourier transform
    frequency_spectrum: dict = fourier.spectrum.convert.to_per_day(fourier.spectrum.frequency(centered_data_column, T))
    fourier.spectrum.plot(frequency_spectrum, "per day")
    
    # extract and export the resonant frequencies
    if (not path_to_output_spectrum is None):
        resonant_frequencies: dict = fourier.spectrum.resonant_frequencies(frequency_spectrum)
        output_data = pd.DataFrame({'frequency (per day)' : resonant_frequencies.keys(), 'amplitude':resonant_frequencies.values()})
        output_data.to_csv(path_to_output_spectrum, index = False)
    
main()