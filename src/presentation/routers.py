from io import BytesIO

from fastapi import APIRouter, Depends, Request, UploadFile, status
from fastapi.responses import StreamingResponse

from src.core.exceptions import ARConverterException
from src.dependencies.dependencies import Container
from src.domain.entities import ARFile
from src.domain.usecases import ConvertFileUseCase
from src.presentation.requests import ARConverterRequest

router = APIRouter(prefix="/convertion", tags=["AR-Convertion"])


@router.post("")
async def make_convertion(
    request: Request,
    file: UploadFile,
    usecase: ConvertFileUseCase = Depends(Container),
) -> StreamingResponse:
    # Создание Pydantic-модели для валидации, что файл существует и у него подходящий заголовок
    file_extension = request.headers.get("X-Extension")
    uploaded_data = ARConverterRequest(extension=file_extension, file=file)

    # Запускаем конвертер. За счет низкой связанности, логика конвертации
    # может быть абсолютно разной, это никак не повлияет на логику API.
    convertion: ARFile = await usecase.convert_file_usecase.invoke(
        uploaded_data
    )

    # Соберем новое имя для результирующего файла.
    old_filename = file.filename
    extension = old_filename.rfind(".")
    new_filename = old_filename[:extension] if extension > 0 else old_filename
    filename_configuration = f'attachment; filename="{new_filename}.usdz"'

    # Подготовим ответ.
    response: StreamingResponse = StreamingResponse(
        BytesIO(convertion.content),
        media_type="application/octet-stream",
        status_code=status.HTTP_201_CREATED,
    )
    # Установим собранное имя файла результату.
    response.headers["Content-Disposition"] = filename_configuration
    return response
