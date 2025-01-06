# reading data and dealing with missing values

import numpy as np

class data:
    
    def has_invalid_values(l: list) -> bool:
        return not all(np.isfinite(l))
    
    def invalid_values(l: list) -> list:
        return list([val for val in l if not np.isfinite(val)])
