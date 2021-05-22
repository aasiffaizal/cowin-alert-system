from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from enum import Enum

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.base import BaseModel as Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get_by_id(self, db: Session, _id: int = None) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == _id).first()

    def get(
        self,
        db: Session,
        filters: Dict[str, Union[str, int, Enum]]
    ) -> Optional[ModelType]:
        return db.query(self.model).filter_by(**filters).first()

    def get_multi(
        self, db: Session, filters: Dict[str, Union[str, int, Enum]] = None,
            skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        query = (db.query(self.model).filter_by(**filters)
                 if filters else db.query(self.model))
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: SchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi(self, db: Session, objs_in: List[SchemaType]) -> None:
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
        db.commit()

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[SchemaType, Dict[str, Any]]
    ) -> ModelType:
        self.set_data_for_update(db_obj, obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_multi(
        self,
        db: Session,
        objs: List[Dict[str, Union[ModelType, Union[SchemaType, Dict[str, Any]]]]],
    ) -> None:
        for obj in objs:
            db_obj = obj.get('db_obj')
            self.set_data_for_update(db_obj, obj.get('obj_in'))
            db.add(db_obj)
        db.commit()

    def remove_with_id(self, db: Session, _id: int) -> ModelType:
        obj = db.query(self.model).get(_id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_multi_with_id(self,  db: Session, ids: List[int]) -> None:
        for _id in ids:
            obj = db.query(self.model).get(_id)
            db.delete(obj)
        db.commit()

    @staticmethod
    def remove(db: Session, obj: ModelType) -> ModelType:
        db.delete(obj)
        db.commit()
        return obj

    @staticmethod
    def remove_multi(db: Session, objs: List[ModelType]) -> None:
        for obj in objs:
            db.delete(obj)
        db.commit()

    @staticmethod
    def set_data_for_update(db_obj, obj_in):
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
