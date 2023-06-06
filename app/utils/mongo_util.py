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
        else:
            raise ValueError(f"Unsupported stage: {self._stage}")

    def build(self):
        return self._pipeline


class Query:
    def __init__(self):
        self._query = {}
        self._current_field = None
        self._current_logical_operator = None
        self._current_comparison_operator = None

    def __getattr__(self, item):
        if item in ["ne", "gt", "lt", "eq"]:
            self._current_comparison_operator = f"${item}"
            return self
        elif item in ["or_", "and_"]:
            self._current_logical_operator = f"${item[:-1]}"
            self._query[self._current_logical_operator] = self._query.get(self._current_logical_operator, [])
            return Query()  # Return new Query object for nested conditions
        else:
            self._current_field = item
            return self

    def __setattr__(self, key, value):
        if key.startswith("_"):
            self.__dict__[key] = value
        else:
            self._add_to_query(key, value)

    def __iadd__(self, other):
        if isinstance(other, Query):
            if self._current_logical_operator:
                self._query[self._current_logical_operator].append(other.build())
        return self

    def _add_to_query(self, key, value):
        if self._current_comparison_operator:
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


if __name__ == "__main__":
    q = Query()
    q.email = "x"  # Simple query
    print(q.build())

    q = Query()
    q.email = "x"
    q.or_.phone = "1234567890"  # Complex query
    print(q.build())

    q = Query()
    q.email = "x"
    q.or_.ne.phone = "1234567890"
    q.and_.status = 1  # Complex query with multiple conditions
    print(q.build())
