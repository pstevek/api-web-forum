from datetime import datetime
from typing import Any, TypeVar, Type, Optional, Dict, Union, List
from app.core.database import db_dependency, persist_db
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload, Query
from sqlalchemy import and_

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository:
    model = ModelType

    def __init__(self, db: db_dependency) -> None:
        self.db = db

    def all(self, skip: int = 0, limit: int = 100, joint_tables=None) -> List[model]:
        query = self.db.query(self.model)
        query = self.add_joint_tables(query, joint_tables)

        return query.filter(self.model.deleted_at.is_(None)) \
            .order_by(self.model.created_at.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()

    def get(self, model_id: int, joint_tables=None) -> Optional[model]:
        query = self.db.query(self.model)
        query = self.add_joint_tables(query, joint_tables)

        return query.filter(
            and_(
                self.model.id == model_id,
                self.model.deleted_at.is_(None)
            )
        ).first()

    def create(self, object_in: CreateSchemaType) -> model:
        request_data = jsonable_encoder(object_in)
        db_obj = self.model(**request_data)

        persist_db(self.db, db_obj)

        return db_obj

    def update(self, db_obj: model, object_in: Union[UpdateSchemaType, Dict[str, Any]]) -> model:
        request_data = jsonable_encoder(db_obj)
        update_data = object_in if isinstance(object_in, dict) else object_in.dict(exclude_unset=True)

        for field in request_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        persist_db(self.db, db_obj)

        return db_obj

    def delete(self, db_obj: model, soft_delete: bool = True) -> None:
        if soft_delete:
            db_obj.deleted_at = datetime.now()
        else:
            self.db.delete(db_obj)
            self.db.commit()

    def add_joint_tables(self, query: Query, joint_tables=None) -> Query:
        if joint_tables is not None and isinstance(joint_tables, list):
            self.db.expunge_all()
            for table in joint_tables:
                if isinstance(table, str):
                    query = query.options(joinedload(getattr(self.model, table)))

        return query
