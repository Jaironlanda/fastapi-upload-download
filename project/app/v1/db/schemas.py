from pydantic import BaseModel
from typing import Optional

class FileDataBase(BaseModel):
    owner_id: int
    filename: Optional[str] = None
    filepath: Optional[str] = None
    filebase64: Optional[str] = None


class FileDataSchemas(FileDataBase):
    file_id: int

    class Config:
        orm_mode = True
