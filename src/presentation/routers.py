from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.responses import JSONResponse

from src.dependencies.dependencies import Container
from src.domain.entities import ARFile
from src.domain.usecases import ConvertFileUseCase
from src.presentation.requests import ARConverterRequest

router = APIRouter(prefix="/convertion", tags=["AR-Convertion"])


@router.post("")
async def make_convertion(
    x_extension: Annotated[Optional[str], Header()],
    file: UploadFile,
    usecase: ConvertFileUseCase = Depends(Container),
) -> JSONResponse:
    # Создание Pydantic-модели для валидации, что файл существует и у него подходящий заголовок
    uploaded_data = ARConverterRequest(extension=x_extension, file=file)

    ar_file_object = ARFile(
        extension=uploaded_data.extension, file=uploaded_data.file
    )
    # Запускаем конвертер. За счет низкой связанности, логика конвертации
    # может быть абсолютно разной, это никак не повлияет на логику API.
    convertion_status: bool = await usecase.convert_file_usecase.invoke(
        ar_file_object
    )

    # Подготовим ответ.
    response: JSONResponse = JSONResponse(
        {"status": "Успешно"} if convertion_status else {"status": "Неудачно"},
        status_code=(
            status.HTTP_201_CREATED
            if convertion_status
            else status.HTTP_204_NO_CONTENT
        ),
    )
    return response
