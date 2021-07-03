from pydantic import BaseModel, validator
from sqlalchemy.orm import Query


class OrmBase(BaseModel):

    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True
