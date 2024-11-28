# mongo_util.py User Guide
The mongo_util.py module provides utilities for building MongoDB aggregation pipelines, constructing queries, and processing cursors with ease. It abstracts MongoDB's syntax into a Pythonic interface, making it accessible for developers.

## Classes
### 1. Pipeline
The Pipeline class enables the creation of MongoDB aggregation pipelines dynamically. It supports multiple aggregation stages, added via attribute assignment.

#### Supported Stages:
- match: Filter documents using conditions.
- unwind: Deconstruct array fields; supports preserveNullAndEmptyArrays.
- lookup: Perform left outer joins with other collections.
- sort: Sort documents in ascending or descending order.
- limit: Limit the number of documents in the result.
- project: Reshape or filter fields in the output.
- custom: Appends stage not above to current pipeline. usage: `pipeline.custom.append(stage)` If using multiple check in match you can use this. 

Example Usage:

```
from nexler.utils.mongo_util import Pipeline, new_pipeline

# Initialize the pipeline
pipe = Pipeline()

# Add stages
pipe.match._id = '605c66b16f3b15a1561d26a6'  # Match documents by '_id'
pipe.unwind.array_field = True               # Unwind array_field with preserved null values
pipe.lookup.from_field = ("collection", "local_field", "foreign_field", "as_field")  # Lookup stage
pipe.sort.age = 1                            # Sort in ascending order by 'age'
pipe.limit = 10                              # Limit output to 10 documents

# Build the pipeline
pipeline = new_pipeline(pipe)
```
### 2. Query
The Query class simplifies the creation of find queries, including support for comparison and logical operators.

#### Supported Operators:
Comparison:
- $eq: Equal to.
- $ne: Not equal to.
- $gt: Greater than.
- $lt: Less than.
Logical:
- $or: Match if any condition is true.
- $and: Match if all conditions are true.
Search:
- $regex: Regular expression matching.
Example Usage:

```
from nexler.utils.mongo_util import Query

# Create a new query
query = Query()

# Define conditions
query.name = 'John'                         # Match documents where 'name' is 'John'
query.ne.status = 0                         # Where 'status' is not 0
query.or_.age = {'$gt': 30}                 # Match age > 30 or
query.or_.active = True                     # active is True

# Build the query
built_query = query.build()
```
## Functions
### 1. new_pipeline(pipeline)
Builds and returns the aggregation pipeline.

Parameters:
- pipeline (Pipeline): A Pipeline object.
Returns:
- list: MongoDB aggregation pipeline.
### 2. process_cursor(cursor, start=None, limit=None, sort=None)
Processes a MongoDB cursor to apply sorting, pagination, and extract results.

Parameters:
- cursor: MongoDB cursor from a find or aggregate operation.
- start (optional): Start index for pagination.
- limit (optional): Limit on the number of results.
- sort (optional): Tuple of (field, order) for sorting.
Returns:
- dict: Contains count (total documents) and data (list of documents).

Example:
```
from nexler.utils.mongo_util import process_cursor

processed = process_cursor(cursor, start=5, limit=10, sort=('_id', -1))
```
### 3. process_value(value)
Processes MongoDB-specific data types:

- Converts ObjectId to a string.
- Formats datetime fields to dd/mm/YYYY.
Parameters:
- value: The value to process.
Returns:
- Processed value.
Complete Example
```
from daba.Mongo import collection
from nexler.utils.mongo_util import Pipeline, Query, new_pipeline, process_cursor

# Initialize a collection
table = collection('x')

# Step 1: Create a pipeline
pipe = Pipeline()
pipe.match.status = 1
pipe.sort.age = -1
pipeline = new_pipeline(pipe)
cursor1 = table.aggregate(pipeline)

# Step 2: Create a query
query = Query()
query.name = 'John'
query.gt.age = 25
built_query = query.build()
cursor2 = table.find(built_query)

# Step 3: Process the cursor
processed = process_cursor(cursor2, start=0, limit=10, sort=('_id', -1))
print(processed)
```

## Summary
With mongo_util.py, you can:

- Dynamically create aggregation pipelines with the Pipeline class.
- Build complex queries with the Query class.
- Easily process cursors and handle MongoDB-specific data formats.