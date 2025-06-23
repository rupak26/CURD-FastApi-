from typing import Optional , Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    message: Optional[str] = None
    statusCode: Optional[int] = None
    datalist: Optional[Any] = None

    class config:
        orm_mode = True