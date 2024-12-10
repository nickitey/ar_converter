from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class ARFile:
    content: UploadFile
