from pydantic import BaseModel
from typing import List

class Subject(BaseModel):
    name: str
    topics: List[str]
