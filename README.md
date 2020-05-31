# ColumnNormalizer
A simple and fast async python script for Postgres that can be used to mass edit a column in a database.

Chunks the data to edit the database concurrently with one connection per chunk.

# Usage
Make sure you're using Python 3.5 or above. Install [asyncpg](https://pypi.org/project/asyncpg/) first. Then edit
```python
start=120000
end=125074 #last element
step=1000
uri='Database URI'
to_normalize='title' #name of column you want to normalize/edit
prim='prim' #name of column with a serial
table='table' #name of table you want to edit
```
to fit your needs. Then just `python normalizer.py` in a terminal of your choice, and it'll do its "magic".

#Other databases

Would this work for other databases? Probably, as long as it has an asynchronous library. Install the library of your choice, and adjust the connection creation and data fetching / updating to fit your library.
