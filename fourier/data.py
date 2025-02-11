# reading data and dealing with missing values
import datetime
import json
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
        
        class config:
            def __init__(self):
                self.__type: str = None
                self.__host_name: str = None
                self.__port: int = None
                self.__user_name: str = None
                self.__password: str = None
                
            def set_type(self, t: str):
                self.__type = t
                
            def get_type(self) -> str:
                return self.__type
                
            def set_host_name(self, host_name: str):
                self.__host_name = host_name
                
            def get_host_name(self) -> str:
                return self.__host_name
            
            def set_port(self, port: int):
                self.__port = port
                
            def get_port(self) -> int:
                return self.__port
                
            def set_user_name(self, user_name: str):
                self.__user_name = user_name
                
            def get_user_name(self) -> str:
                return self.__user_name
                
            def set_password(self, password: str):
                self.__password = password
                
            def get_password(self) -> str:
                return self.__password
                
            def read(file_path: str):
                assert os.path.isfile(file_path), "Configuration file doesn't exist: " + file_path
                
                return_config = data.db.config()
                with open(file_path, 'r') as j:
                    config_json = json.loads(j.read())
                    
                    return_config.set_type(config_json["settings"]["database"]["type"])
                    return_config.set_host_name(config_json["settings"]["database"]["host_name"])
                    return_config.set_port(config_json["settings"]["database"]["port"])
                    return_config.set_user_name(config_json["settings"]["database"]["user_name"])
                    return_config.set_password(config_json["settings"]["database"]["password"])
                
                return return_config
        
        def connect():
            from sqlalchemy import create_engine
    
            config_path: str = os.path.join("..", "..", "py-config.json")
            db_config = data.db.config.read(config_path)
    
            # Database connection parameters
            database_type: str = db_config.get_type()
            user_name: str = db_config.get_user_name()
            password: str = db_config.get_password()
            host_name: str = db_config.get_host_name()
            port: int = db_config.get_port()
    
            # Create a connection string
            connection_string: str = f'{database_type}://{user_name}:{password}@{host_name}:{port}'
            
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