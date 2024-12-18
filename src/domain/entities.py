from dataclasses import dataclass
from typing import Optional

from fastapi import UploadFile


@dataclass
class ARFile:
    extension: Optional[str]
    file: Optional[UploadFile]
