from src.data.repositories import ARFileRepository
from src.domain.entities import ARFile


class ConvertFileUseCase:
    def __init__(self, file_repo: ARFileRepository):
        self._file_repo = file_repo()

    async def invoke(self, received_content) -> ARFile:
        byte_content = await self._file_repo.convert(received_content)
        return ARFile(content=byte_content)
