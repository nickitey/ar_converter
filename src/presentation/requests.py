from typing import Optional

from fastapi import UploadFile, status
from pydantic import BaseModel, field_validator, model_validator

from src.core.exceptions import ARConverterException


class ARConverterRequest(BaseModel):
    extension: Optional[str]
    file: Optional[UploadFile]

    @field_validator("extension")
    @classmethod
    def extension_is_correct(cls, ext):
        if ext is None:
            raise ARConverterException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Please provide X-Extension request header.",
            )
        if ext not in ("glb", "fbx"):
            raise ARConverterException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="This type of files is unsupported.",
            )
        return ext

    @field_validator("file")
    @classmethod
    def file_is_present(cls, file):
        if file is None:
            raise ARConverterException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide file to convert.",
            )
        return file

    @model_validator(mode="after")
    def file_and_extension_match(self):
        try:
            received_filename = self.file.filename.lower()
            received_extension = self.extension.lower()
            assert received_filename.endswith(received_extension)
        except AssertionError:
            raise ARConverterException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File extension does not match with X-Extension header.",
            )
        return self
