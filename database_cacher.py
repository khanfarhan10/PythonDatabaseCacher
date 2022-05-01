import sqlite3
import hashlib

class databaseCacher:
    def __init__(self, dbFileName = "cachingDataBase.sqlite", APIVersion = None) -> None:
        self.dbFileName = dbFileName
        if APIVersion is None:
            self.APIVersion = "1.0" # TODO : Change this to dynamically created version
    
    def hashingFunction(self, string_given):
        return hashlib.sha512(string_given.strip().encode()).hexdigest()

    # input -> input_file_name -> output -> output_file_name
    # versioning for changes -> watch god reload file reloader -> hash maker
    # decorator wrapper
    # (functionname + filename) -> tablename
    # columnNames -> input hash (args, kwargs), dateCreated, APIVersion
DB_CACHER = databaseCacher()

def dbCacher(*args_std, **kwargs_std):
    def standard_db_wrapper(func, *args, **kwargs):
        print("Before calling " + func.__name__)
        print(dir(func))
        print( args, kwargs)
        print( args_std, kwargs_std)
        func( *args, **kwargs)
        print("After calling " + func.__name__)
    return standard_db_wrapper
    
if __name__ == "__main__":
    print(DB_CACHER.hashingFunction("Hello World"))
    