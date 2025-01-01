from bson import ObjectId
from typing import Type, TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseClass(Generic[T]):
    def __init__(self, model: Type[T], dataCol):
        self.collection = dataCol
        self.model = model

    def save(self, data: T) -> ObjectId:
        if data.id is None:  # Insert operation
            data_dict = data.dict(by_alias=True, exclude_unset=True)
            data_dict.pop("_id", None)
            result = self.collection.put(data_dict)
            data.id = result.inserted_id
            return data.id
        else:  # Update operation
            query = {"_id": data.id}
            update_data = {"$set": data.dict(by_alias=True, exclude_unset=True)}
            self.collection.set(query, update_data)
            return data.id

    def get(self, query: dict) -> Optional[T]:
        document = self.collection.getOne(query)
        if document:
            return self.model(**document)
        return None

    def get_all(self, query=None) -> list[T]:
        if query is None:
            query = {}
        return [self.model(**doc) for doc in self.collection.find(query)]

    def delete(self, query: dict) -> int:
        result = self.collection.deleteOne(query)
        return result.deleted_count

    def count(self, query=None) -> int:
        if query is None:
            query = {}
        return self.collection.count(query)

    def aggregate(self, query=None) -> list:
        if query is None:
            query = {}
        return [doc for doc in self.collection.find(query)]
