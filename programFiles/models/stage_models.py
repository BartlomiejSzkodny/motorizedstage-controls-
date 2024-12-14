from typing import TypeVar, Generic

from pydantic import BaseModel

from app.enums.service_errors import ServiceError

T = TypeVar("T", bound=BaseModel)


class DaoError(BaseModel):
    error: ServiceError
    description: str
    return_status: int = 0


class DaoResponse(BaseModel, Generic[T]):
    data: T
    error: DaoError
