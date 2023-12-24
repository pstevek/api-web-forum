from database import db_dependency, Base
from fastapi import HTTPException, status


def get_model_by_id(db: db_dependency, model: Base, id: int) -> Base:
    base_model = db.query(model).filter(model.id == id).first()

    if not base_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")

    return base_model
