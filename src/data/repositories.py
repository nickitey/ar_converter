import io
import aspose.threed as a3d

from src.domain.repositories import IARFileRepository
from src.core.exceptions import TrialException

TrialException.suppress_trial_exception = True

class ARFileRepository(IARFileRepository):
    async def convert(self, arfile):
        scene = a3d.Scene()
        file_bytes = io.BytesIO(await arfile.read())
        try:
            worker = scene.open(stream=file_bytes)
            result = scene.save(stream=worker, format=a3d.FileFormat.USDZ)
            scene.close()
        finally:
            print('vse')
        return result
