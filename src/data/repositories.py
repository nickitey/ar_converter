import subprocess
import aiofiles
import io

from src.domain.repositories import IARFileRepository


class ARFileRepository(IARFileRepository):
    async def convert(self, arfile):
        content = await arfile.read()
        name = arfile.filename
        print(name)
        try:
            async with aiofiles.open(name, 'wb') as tempfile:
                await tempfile.write(content)
            subprocess.run(
                ["usdzconvert", name, "resultfile.usdz"]
            )
        except subprocess.CalledProcessError:
            raise Exception(
                f'Unable to convert {self._source_file_path} to {self._destination_file_path}',
            )
        else:
            with open("resultfile.usdz", "rb") as resultfile:
                content = resultfile.read()
            return content
