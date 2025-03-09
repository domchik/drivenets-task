from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str

class DataResponse(BaseModel):
    data: List[Item] 