FROM smthfor/gltf-to-usdz-node

WORKDIR /usr/ar-converter

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --verbose
    
COPY src/ src/

CMD ["uvicorn", "src:app", "--workers", "4"]
