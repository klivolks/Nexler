import copy
import datetime
from nexler.utils import dt_util
from bson import ObjectId


class Pipeline:
    def __init__(self):
        self._pipeline = []
        self._stage = None

    def __getattr__(self, stage):
        self._stage = stage
        return self

    def __setattr__(self, field, value):
        if field in ("_stage", "_pipeline"):
            super().__setattr__(field, value)
        elif self._stage == "match":
            self._pipeline.append({f"${self._stage}": {field: ObjectId(value) if field == "_id" else value}})
        elif self._stage == "unwind":
            self._pipeline.append({f"${self._stage}": {"path": f"${field}", "preserveNullAndEmptyArrays": value}})
        elif self._stage == "lookup":
            self._pipeline.append(
                {f"${self._stage}": {"from": field, "localField": value[0], "foreignField": value[1], "as": value[2]}})
        elif self._stage == "sort":
            self._pipeline.append({f"${self._stage}": {field: value}})
        elif self._stage == "limit":
            self._pipeline.append({f"${self._stage}": value})
        elif self._stage == "project":
            self._pipeline.append({f"${self._stage}": {field: value}})
        else:
            raise ValueError(f"Unsupported stage: {self._stage}")

    def build(self):
        return self._pipeline

    @property
    def custom(self):
        return self._pipeline

    def __deepcopy__(self, memo):
        # Create a new Pipeline instance
        copied_pipeline = Pipeline()
        # Deep copy the internal _pipeline list
        copied_pipeline._pipeline = copy.deepcopy(self._pipeline, memo)
        # Return the copied instance
        return copied_pipeline


class Query:
    def __init__(self):
        self._query = {}
        self._current_field = None
        self._current_logical_operator = None
        self._current_comparison_operator = None
        self._search_flag = False

    def __getattr__(self, item):
        if item in ["ne", "gt", "lt", "eq"]:
            self._current_comparison_operator = f"${item}"
            return self
        elif item in ["or_", "and_"]:
            self._current_logical_operator = f"${item[:-1]}"
            self._query[self._current_logical_operator] = self._query.get(self._current_logical_operator, [])
            return Query()  # Return new Query object for nested conditions
        elif item == "search":
            self._search_flag = True
            return self
        else:
            self._current_field = item
            return self

    def __setattr__(self, key, value):
        if key == "_id":
            self._add_to_query(key, ObjectId(value))
        elif key.startswith("_"):
            self.__dict__[key] = value
        else:
            self._add_to_query(key, value)

    def __iadd__(self, other):
        if isinstance(other, Query):
            if self._current_logical_operator:
                self._query[self._current_logical_operator].append(other.build())
        return self

    def _add_to_query(self, key, value):
        if self._search_flag:
            self._query[key] = {"$regex": value}
            self._search_flag = False
        elif self._current_comparison_operator:
            comparison = {self._current_comparison_operator: value}
            self._query[key] = comparison
            self._reset_operators()
        else:
            self._query[key] = value

    def _reset_operators(self):
        self._current_field = None
        self._current_comparison_operator = None

    def build(self):
        return self._query


def new_pipeline(pipeline):
    return pipeline.build()


def process_cursor(cursor, start=None, limit=None, sort=None):
    if start is not None:
        cursor = cursor.skip(start)
    if limit is not None:
        cursor = cursor.limit(limit)
    if sort is not None:
        cursor = cursor.sort(*sort)

    data = [doc for doc in cursor]
    count = len(data)

    return {"count": count, "data": data}


def process_value(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime.datetime):
        return dt_util.human_date(value, "%d/%m/%Y")
    else:
        return value


if __name__ == "__main__":
    # q = Query()
    # q._id = "x"  # Simple query
    # print(q.build())
    #
    # q = Query()
    # q.email = "x"
    # q1 = q.or_
    # q1.phone = "1234567890"  # Complex query
    # q += q1
    # print(q.build())
    #
    # q = Query()
    # q.email = "x"
    # q1 = q.or_
    # q1.ne.phone = "1234567890"
    # q += q1
    # q.status = 1  # Complex query with multiple conditions
    # print(q.build())

    q = Query()
    q1 = q.search
    q1.name = 'Jo'
    q += q1
    print(q.build())
