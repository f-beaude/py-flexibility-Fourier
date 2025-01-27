# reading data and dealing with missing values
import datetime
import os.path

import numpy as np
import pandas as pd

class data:
    
    def has_invalid_values(l: list) -> bool:
        return not all(np.isfinite(l))
    
    def invalid_values(l: list) -> list:
        return list([val for val in l if not np.isfinite(val)])

    class csv:
        # extract data from a CSV file (assuming that the first row includes column names)
        def read (file_path: str, column_name: str):
            
            assert os.path.isfile(file_path), "File doesn't exist: " + file_path
    
            csv_data_full = pd.read_csv(file_path, sep=',', header = 0)
            
            assert column_name in csv_data_full.keys(), "Column doesn't exist: " + column_name
            return pd.to_numeric(csv_data_full[column_name], errors = 'raise')
    
    class db:
        def connect():
            from sqlalchemy import create_engine
    
            # Database connection parameters
            database_type: str = 'mysql'
            username: str = 'USER'
            password: str = 'PASSWORD'
            host: str = 'HOST'
            port: int = 3306
    
            # Create a connection string
            connection_string: str = f'{database_type}://{username}:{password}@{host}:{port}'
            
            # Create a database engine
            return create_engine(connection_string)
    
        def query(sql_query: str):
            engine = data.db.connect()
            return pd.read_sql(sql_query, engine)
    
        def extract_data_from_query_results (query_results, datetime_column_name: str, value_column_name: str, timedelta: datetime.timedelta):
            column_names: list = [datetime_column_name, value_column_name]
            assert all([name in query_results for name in column_names]), "Missing columns from SQL results: " + ", ".join([name for name in column_names if name not in query_results])
            
            query_results[datetime_column_name] = pd.to_datetime(query_results[datetime_column_name], format="%Y-%m-%d %H:%M:%S")
            
            data = []
            date_min: datetime.datetime = min(query_results[datetime_column_name])
            date_max: datetime.datetime = max(query_results[datetime_column_name])
            date_current: datetime.datetime = date_min
            while date_current <= date_max:
                value: float = float('nan')
                if date_current in query_results[datetime_column_name].values:
                    value: float = query_results[query_results[datetime_column_name]==date_current][value_column_name].values[0]
                
                data.append(value)
                date_current += timedelta
            return data