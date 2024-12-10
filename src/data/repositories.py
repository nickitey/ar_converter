from src.domain.repositories import IARFileRepository


class ARFileRepository(IARFileRepository):
    async def convert(self, arfile):
        print(arfile.file)
        return "Hello, world".encode()
