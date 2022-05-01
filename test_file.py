from database_cacher import dbCacher

@dbCacher(dbFileName = "cachingDataBase.sqlite")
def add_one(x):
    print (x + 1)

add_one( 1)