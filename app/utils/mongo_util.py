from bson import ObjectId
import re


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

    def __setattr__(self, field, value):
        if field in ("_limit", "_start", "_sort"):
            super().__setattr__(field, value)
        elif field.startswith("_"):
            if field == "_id":
                self._query[field] = ObjectId(value)
            else:
                super().__setattr__(field, value)
        elif field == "search":
            self._query[value[0]] = re.compile(value[1], re.IGNORECASE)
        else:
            self._query[field] = value

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
