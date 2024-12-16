import os
import subprocess

import aiofiles
from fastapi import status

from src.core.exceptions import ARConverterException
from src.domain.repositories import IARFileRepository


class ARFileRepository(IARFileRepository):
    async def convert(self, arfile):
        content, extension = arfile.file, arfile.extension
        sourcefile_name = content.filename.lower()
        async with aiofiles.open(sourcefile_name, "wb") as tempfile:
            await tempfile.write(await content.read())
        if extension.lower() == "fbx":
            try:
                subprocess.run(["fbx2glb", "-b", sourcefile_name])

            except subprocess.CalledProcessError:
                raise ARConverterException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Unable to convert {sourcefile_name} into a USDZ-file. File seems to be corrupted.",
                )
            os.remove(sourcefile_name)
            sourcefile_name = sourcefile_name.replace(extension, "glb")
        try:
            subprocess.run(["usdzconvert", sourcefile_name, "resultfile.usdz"])
        except subprocess.CalledProcessError:
            raise ARConverterException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unable to convert {sourcefile_name} into a USDZ-file. File seems to be corrupted.",
            )
        else:
            resultfile = "resultfile.usdz"
            async with aiofiles.open(resultfile, "rb") as result:
                content = await result.read()
            os.remove(sourcefile_name)
            os.remove(resultfile)
            return content
