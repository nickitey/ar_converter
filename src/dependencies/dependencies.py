from src.data.repositories import ARFileRepository
from src.domain.usecases import ConvertFileUseCase


class Container:
    convert_file_usecase = ConvertFileUseCase(ARFileRepository)
