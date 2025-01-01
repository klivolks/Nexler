from nexler.model.base_model import MongoBaseModel
from nexler.model.base_class import BaseClass
from datetime import datetime
from bson import ObjectId
from daba.Mongo import collection
from typing import Optional
from nexler.utils import dt_util
from nexler.services.AuthService import user


class SampleStructureModel(MongoBaseModel):
    data: Optional[str]
    Status: str = 'active'
    CreatedAt: Optional[datetime] = dt_util.get_current_time()
    UpdatedAt: datetime = dt_util.get_current_time()
    CreatedBy: Optional[ObjectId] = user.Id
    isDeleted: bool = False


data_collection = collection("SampleStructure")

handler = BaseClass(SampleStructureModel, data_collection)
