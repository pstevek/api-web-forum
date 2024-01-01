from datetime import datetime
from typing import Any, TypeVar, Type, Optional, Dict, Union
from app.core.database import db_dependency, persist_db
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository:
    def __init__(self, model: Type[ModelType], db: db_dependency) -> None:
        self.model = model
        self.db = db

    def get(self, model_id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == model_id).first()

    def create(self, object_in: CreateSchemaType) -> ModelType:
        request_data = jsonable_encoder(object_in)
        db_obj = self.db.model(**request_data)

        persist_db(self.db, db_obj)

        return db_obj

    def update(self, db_obj: ModelType, object_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        print("*** debug (before) ***", db_obj.__dict__)
        request_data = jsonable_encoder(db_obj)
        update_data = object_in if isinstance(object_in, dict) else object_in.dict(exclude_unset=True)

        for field in request_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        print("*** debug (after) ***", db_obj.__dict__)

        persist_db(self.db, db_obj)

        return db_obj

    def delete(self, db_obj: ModelType, soft_delete: bool = True) -> None:
        if soft_delete:
            db_obj.deleted_at = datetime.now()
        else:
            self.db.delete(db_obj)
            self.db.commit()
