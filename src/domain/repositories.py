import abc


class IARFileRepository(abc.ABC):
    @abc.abstractmethod
    async def convert(self, arfile: bytes): ...
