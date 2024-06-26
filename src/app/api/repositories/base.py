from datetime import datetime
from typing import Any, TypeVar, Optional, Dict, Union, List, Type
from app.core.database import use_database_session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload, Query
from sqlalchemy import and_

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository:
    model: Type[ModelType] = BaseModel

    def __init__(self) -> None:
        with use_database_session() as session:
            self.db = session

    def all(
            self,
            filtered: Query,
            skip: int = 0,
            limit: int = 10,
            orderby: Query | None = None,
            joint_tables: list | None = None
    ) -> List[model]:
        query = self.db.query(self.model)
        query = self.add_joint_tables(query, joint_tables)

        if orderby is None:
            orderby = self.model.created_at.desc()

        return query.filter(filtered) \
            .order_by(orderby) \
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

        self.persist_db(db_obj)

        return db_obj

    def update(self, db_obj: model, object_in: Union[UpdateSchemaType, Dict[str, Any]]) -> model:
        request_data = jsonable_encoder(db_obj)
        update_data = object_in if isinstance(object_in, dict) else object_in.dict(exclude_unset=True)

        for field in request_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.persist_db(db_obj)

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

    def persist_db(self, obj: model) -> None:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
