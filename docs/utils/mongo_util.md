Here is the user documentation for `mongo_util.md`, describing the classes, methods, and their usage:

---

# Mongo Utility Documentation (`mongo_util.md`)

This utility provides helper classes and functions to simplify the construction and processing of MongoDB pipelines, queries, and cursors.

---

## **Classes and Methods**

### **Pipeline Class**
The `Pipeline` class is used to construct MongoDB aggregation pipelines in a structured and reusable manner.

#### **Methods & Properties**
1. **`custom` (Property)**
   - Provides direct access to the `_pipeline` list for appending custom stages.
   - Example:
     ```python
     pipeline = Pipeline()
     pipeline.custom.append({'$match': {'isDeleted': False}})
     ```

2. **`build()`**
   - Builds and returns the pipeline as a list of stages.
   - Example:
     ```python
     pipeline = Pipeline()
     pipeline.match.field = "value"
     final_pipeline = pipeline.build()
     print(final_pipeline)  # [{'$match': {'field': 'value'}}]
     ```

3. **Dynamic Stage Construction**
   - Use attribute access to define pipeline stages dynamically. Supported stages:
     - `$match`: Filters documents.
       ```python
       pipeline = Pipeline()
       pipeline.match.field = "value"
       ```
     - `$unwind`: Deconstructs an array field into separate documents.
       ```python
       pipeline.unwind.field = True  # `preserveNullAndEmptyArrays` is set to True
       ```
     - `$lookup`: Joins data from another collection.
       ```python
       pipeline.lookup.collection = ("localField", "foreignField", "asField")
       ```
     - `$sort`: Sorts documents.
       ```python
       pipeline.sort.field = -1  # -1 for descending, 1 for ascending
       ```
     - `$limit`: Limits the number of documents.
       ```python
       pipeline.limit = 10
       ```
     - `$project`: Projects specific fields.
       ```python
       pipeline.project.field = 1
       ```

4. **Deep Copy Support**
   - The `Pipeline` class supports deep copying via `copy.deepcopy()`.
   - Example:
     ```python
     import copy
     pipeline = Pipeline()
     pipeline.match.field = "value"
     copied_pipeline = copy.deepcopy(pipeline)
     ```

---

### **Query Class**
The `Query` class provides utilities to construct MongoDB filter queries with support for logical and comparison operators.

#### **Methods & Features**
1. **Dynamic Attribute Access**
   - Define fields and operators dynamically.
   - Example:
     ```python
     query = Query()
     query.field = "value"
     query.ne.other_field = "other_value"
     ```

2. **Logical Operators**
   - Supports `$or` and `$and` for combining conditions.
   - Example:
     ```python
     query = Query()
     query.or_ += Query().field.eq = "value"
     query.or_ += Query().other_field.ne = "other_value"
     combined_query = query.build()
     print(combined_query)
     # {'$or': [{'field': {'$eq': 'value'}}, {'other_field': {'$ne': 'other_value'}}]}
     ```

3. **Comparison Operators**
   - Supported operators: `$eq`, `$ne`, `$gt`, `$lt`.
   - Example:
     ```python
     query = Query()
     query.field.gt = 10
     ```

4. **Regex Search**
   - Enables regex-based search using the `search` attribute.
   - Example:
     ```python
     query = Query()
     query.search.field = "pattern"
     ```

5. **`build()`**
   - Builds and returns the final query.
   - Example:
     ```python
     query = Query()
     query.field = "value"
     print(query.build())  # {'field': 'value'}
     ```

---

### **Utility Functions**

#### **`new_pipeline(pipeline)`**
Builds and returns the pipeline stages from a `Pipeline` instance.

- **Parameters**: 
  - `pipeline` (Pipeline): A `Pipeline` instance.
- **Returns**: `list`
- **Example**:
  ```python
  pipeline = Pipeline()
  pipeline.match.field = "value"
  stages = new_pipeline(pipeline)
  print(stages)  # [{'$match': {'field': 'value'}}]
  ```

---

#### **`process_cursor(cursor, start=None, limit=None, sort=None)`**
Processes a MongoDB cursor by applying pagination and sorting.

- **Parameters**:
  - `cursor`: MongoDB cursor.
  - `start` (int): Number of documents to skip.
  - `limit` (int): Maximum number of documents to retrieve.
  - `sort` (tuple): Sorting criteria (field, order).
- **Returns**: `dict` with `count` (number of documents) and `data` (list of documents).
- **Example**:
  ```python
  processed = process_cursor(cursor, start=10, limit=5, sort=("field", 1))
  print(processed)  # {'count': 5, 'data': [...]}
  ```

---

#### **`process_value(value)`**
Processes a MongoDB document value for better readability.

- **Parameters**:
  - `value`: Any value to process (e.g., `ObjectId`, `datetime`).
- **Returns**: A processed string or the original value.
- **Example**:
  ```python
  from bson import ObjectId
  print(process_value(ObjectId()))  # "5f43a1a..."
  ```

---

### Example Usage

```python
from mongo_util import Pipeline, Query, new_pipeline, process_cursor

# Construct a pipeline
pipeline = Pipeline()
pipeline.match.isDeleted = False
pipeline.unwind.field = True
pipeline.sort.createdAt = -1
final_pipeline = new_pipeline(pipeline)

# Construct a query
query = Query()
query.field.eq = "value"
filter_query = query.build()

# Process a cursor
result = process_cursor(cursor, start=0, limit=10, sort=("createdAt", -1))
```

This documentation covers all methods and classes provided in the utility.