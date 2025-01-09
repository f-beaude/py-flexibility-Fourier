import numpy as np
import os.path
import math
import unittest
import sys

# import the package using path to directory
sys.path.append (os.path.join('..', '..'))
import fourier

class data:
    
    def all ():
        data.Data().all()

    class Data(unittest.TestCase):
        def all(self):
            self.__invalid_values()

        # Manage invalid numerical values
        def __invalid_values(self):
            
            l1: list = [1.244, 5, 10, -5.89879, 8887986876.56]
            self.assertFalse(fourier.data.has_invalid_values(l1))
            
            l_nan: list = np.append(l1, np.nan)
            self.assertTrue(fourier.data.has_invalid_values(l_nan))
            invalid_values_nan: list = fourier.data.invalid_values(l_nan)
            self.assertEqual(len(invalid_values_nan), 1)
            self.assertTrue(math.isnan(invalid_values_nan[0]))
            
            l_infinity: list = np.append(l1, np.inf)
            self.assertTrue(fourier.data.has_invalid_values(l_infinity))
            self.assertEqual(fourier.data.invalid_values(l_infinity), [np.inf])
            
            l_both: list = np.append(np.append(l1, np.nan), np.inf)
            self.assertTrue(fourier.data.has_invalid_values(l_both))
            invalid_values_both: list = fourier.data.invalid_values(l_both)
            # Python considers that the list has length 1, despite having two elements
            #self.assertEqual(len(invalid_values_nan), 2)
            self.assertTrue(math.isnan(invalid_values_nan[0]))
            self.assertTrue(np.inf in invalid_values_both)

def main():
    data.all()
#main()
