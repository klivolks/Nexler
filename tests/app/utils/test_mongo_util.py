import unittest
from unittest.mock import MagicMock, Mock
from bson import ObjectId
from app.utils.mongo_util import Pipeline, Query, new_pipeline, process_cursor


class TestMongoUtil(unittest.TestCase):
    def setUp(self):
        self.sample_id = '605c66b16f3b15a1561d26a6'
        self.match_stage = {"$match": {"_id": ObjectId(self.sample_id)}}
        self.unwind_stage = {"$unwind": {"path": "$field", "preserveNullAndEmptyArrays": True}}
        self.lookup_stage = {"$lookup": {"from": "from_field", "localField": "local", "foreignField": "foreign", "as": "as_field"}}
        self.sort_stage = {"$sort": {"field": 1}}

    def test_pipeline(self):
        pipe = Pipeline()
        pipe.match._id = self.sample_id
        self.assertEqual(pipe.build(), [self.match_stage])

        pipe = Pipeline()
        pipe.unwind.field = True
        self.assertEqual(pipe.build(), [self.unwind_stage])

        pipe = Pipeline()
        pipe.lookup.from_field = ("local", "foreign", "as_field")
        self.assertEqual(pipe.build(), [self.lookup_stage])

        pipe = Pipeline()
        pipe.sort.field = 1
        self.assertEqual(pipe.build(), [self.sort_stage])

    def test_query(self):
        query = Query()
        query._id = self.sample_id
        self.assertEqual(query.build(), {"_id": ObjectId(self.sample_id)})

        query = Query()
        query.name = 'John'
        self.assertEqual(query.build(), {"name": 'John'})

        query = Query()
        q1 = query.search
        q1.name = 'Jo'
        query += q1
        self.assertTrue('name' in query.build())
        self.assertTrue(query.build()['name'], {'$regex': 'Jo'})

    def test_new_pipeline(self):
        pipe = Pipeline()
        pipe.match._id = self.sample_id
        self.assertEqual(new_pipeline(pipe), [self.match_stage])

    def test_process_cursor(self):
        cursor = MagicMock()
        cursor.skip = MagicMock(return_value=cursor)
        cursor.limit = MagicMock(return_value=cursor)
        cursor.sort = MagicMock(return_value=cursor)
        cursor.__iter__ = Mock(return_value=iter([{'doc': 1}, {'doc': 2}]))

        processed = process_cursor(cursor, start=10, limit=5, sort=('age', 1))
        cursor.skip.assert_called_once_with(10)
        cursor.limit.assert_called_once_with(5)
        cursor.sort.assert_called_once_with('age', 1)
        self.assertEqual(processed, {"count": 2, "data": [{'doc': 1}, {'doc': 2}]})


if __name__ == '__main__':
    unittest.main()
