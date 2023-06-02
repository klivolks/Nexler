# `mongo_util.py` User Documentation

The `mongo_util.py` module simplifies MongoDB operations in Python. It provides classes and functions for creating MongoDB pipelines and queries, and processing MongoDB cursors, catering to a wide range of MongoDB aggregation stages and query operations.

## Classes

### 1. Pipeline
The `Pipeline` class assists in the creation of MongoDB aggregation pipelines. It supports multiple aggregation stages like `match`, `unwind`, `lookup`, and `sort`.

**Usage:**

```python
from app.utils.mongo_util import Pipeline, new_pipeline

# Create a new pipeline instance
pipe = Pipeline()

# Add a match condition
pipe.match._id = '605c66b16f3b15a1561d26a6'

# Add an unwind condition
pipe.unwind.array_field = True  # preserve null and empty arrays

# Add a lookup condition
pipe.lookup.from_field = ("from_collection", "local_field", "foreign_field", "as_field")

# Add a sort condition
pipe.sort.age = 1  

# Construct the pipeline
pipeline = new_pipeline(pipe)  
```

### 2. Query
The `Query` class helps to construct MongoDB find queries. It supports several query operations like setting conditions on fields, regular expression search, and specific operations on `_id` field.

**Usage:**

```python
from app.utils.mongo_util import Query

# Create a new Query instance
query = Query()

# Set conditions
query._id = '605c66b16f3b15a1561d26a6'  
query.name = 'John'  

# Set a search condition
query.search = ('name', 'Jo') # search for 'Jo' in the 'name' field, case insensitive

# Build the query
built_query = query.build() 
```

## Functions

### 1. new_pipeline(pipeline)
This function takes a `Pipeline` object and returns the constructed pipeline.

### 2. process_cursor(cursor, start=None, limit=None, sort=None)
This function processes a MongoDB cursor, with optional parameters for start, limit, and sort. It returns a dictionary with the count of documents and the documents themselves.

**Usage:**

```python
from app.utils.mongo_util import process_cursor

# Assuming 'cursor' is a pymongo.cursor.Cursor instance returned by a find() call
processed = process_cursor(cursor, start=10, limit=5, sort=('age', 1))
```

## Example:

```python
from daba.Mongo import collection
from app.utils.mongo_util import Pipeline, Query, new_pipeline, process_cursor

table = collection('x')

# Create a pipeline
pipe = Pipeline()
pipe.match._id = '605c66b16f3b15a1561d26a6'
pipe.sort.age = 1
pipeline = new_pipeline(pipe)

# Use the pipeline in an aggregation
cursor1 = table.find(pipeline)

# Create a query
query = Query()
query._id = '605c66b16f3b15a1561d26a6'
query.name = 'John'
built_query = query.build()

# Use the query in a find operation
cursor2 = table.get(built_query)

# Process the cursor
processed = process_cursor(cursor2, start=10, limit=10, sort=('_id', -1))
```

In this example, a `Pipeline` and `Query` object are created to interact with a MongoDB collection. The objects are then used in `aggregate` and `find` operations, respectively. The cursors returned from these operations are processed using the `process_cursor` function.