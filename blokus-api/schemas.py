from pydantic import BaseModel
from typing import List, Optional

class PieceName(BaseModel):
    name: str
