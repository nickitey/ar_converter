import subprocess

import aiofiles
from fastapi import status

from src.core.exceptions import ARConverterException
from src.domain.repositories import IARFileRepository


class ARFileRepository(IARFileRepository):
    async def convert(self, arfile):
        content, header_extension = arfile.file, arfile.extension
        sourcefile_name = content.filename

        old_filename = content.filename
        file_extension = old_filename.rfind(".")
        new_filename = (
            old_filename[:file_extension]
            if file_extension > 0
            else old_filename
        )

        async with aiofiles.open(sourcefile_name, "wb") as tempfile:
            await tempfile.write(await content.read())
        if header_extension.lower() == "fbx":
            try:
                subprocess.run(["fbx2glb", "-b", sourcefile_name])

            except subprocess.CalledProcessError:
                raise ARConverterException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Unable to convert {sourcefile_name} into a USDZ-file. File seems to be corrupted.",
                )

            sourcefile_name = sourcefile_name.replace(header_extension, "glb")
        try:
            subprocess.run(
                ["usdzconvert", sourcefile_name, f"{new_filename}.usdz"]
            )
        except subprocess.CalledProcessError:
            raise ARConverterException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unable to convert {sourcefile_name} into a USDZ-file. File seems to be corrupted.",
            )
        return True
