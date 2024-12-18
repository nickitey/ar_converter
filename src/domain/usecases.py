from src.data.repositories import ARFileRepository


class ConvertFileUseCase:
    def __init__(self, file_repo: ARFileRepository):
        self._file_repo = file_repo()

    async def invoke(self, received_content) -> bool:
        return await self._file_repo.convert(received_content)
