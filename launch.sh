#!/bin/sh
export $(grep -v '^#' .env | xargs -d '\n')
cd converter
echo "$(date +%H:%M:%S\ %d.%m.%Y): Приступаю к сборке базового образа конвертера"
docker build -t ar_converter-converter -f Dockerfile .
echo "$(date +%H:%M:%S\ %d.%m.%Y): Сборка базового образа конвертера закончена"
cd ..
echo "$(date +%H:%M:%S\ %d.%m.%Y): Приступаю к сборке образа веб-сервера"
docker build -t ar-converter-image -f Dockerfile .
echo "$(date +%H:%M:%S\ %d.%m.%Y): Сборка образа веб-сервера закончена"
echo "$(date +%H:%M:%S\ %d.%m.%Y): Запускаю контейнер с сервером. Сервер слушает запросы, поступающие на порт $CONTAINER__EXTERNAL_PORT хоста"
docker run --rm \
	--name ar_converter \
    -v $PWD/src/:/usr/ar-converter/src/ \
    -p $CONTAINER__EXTERNAL_PORT:$UVICORN__PORT \
	--env-file .env \
	ar-converter-image \
	python -m uvicorn src:app --host $UVICORN__HOST --port $UVICORN__PORT --workers $UVICORN__WORKERS

