from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, field_validator


class ARConverterRequest(BaseModel):
    file: Optional[UploadFile]

    @staticmethod
    @field_validator("file")
    def file_is_present(v):
        if v is None:
            raise AttributeError("File not found")
        return v
