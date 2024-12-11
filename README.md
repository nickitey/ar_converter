#ar_converter

## gltf-to-usdz

https://hub.docker.com/r/smthfor/gltf-to-usdz-node

https://github.com/google/usd_from_gltf

Установка непосредственно конвертера разбивается на два этапа:
- установка непосредственно [инструмента](https://github.com/PixarAnimationStudios/USD) для работы с USD-файлами;
- установка конвертера от Google.

Первый этап завершается успехом, Docker-образ на основе файла `Dockerfile_usd` успешно собирается по команде
```bash
docker build -t baseusd -f Dockerfile_usd .
```

Для второго этапа подготовлен файл `Dockerfile_gltf` на основе `Dockerfile` по ссылке № 1 и в соответствии с инструкциями по установке по ссылке № 2.

Все попытки установки завершались неуспешно, ошибка связана с неправильными/некорректными/неактуальными исходниками 3D-компрессора [Draco](https://github.com/google/draco):
```bash
108.7 /usr/local/ufg/src/draco-1.3.5/src/draco/core/hash_utils.h:57:3: note: ‘size_t’ is defined in header ‘<cstddef>’; did you forget to ‘#include <cstddef>’?
108.7 gmake[2]: *** [CMakeFiles/draco_core.dir/build.make:188: CMakeFiles/draco_core.dir/src/draco/core/hash_utils.cc.o] Error 1
108.7 gmake[1]: *** [CMakeFiles/Makefile2:563: CMakeFiles/draco_core.dir/all] Error 2
108.7 gmake: *** [Makefile:136: all] Error 2
108.7 
108.7   DRACO: ERROR: Command failed: cmake --build . --config Release --target install --
108.7   DRACO: See log at: /usr/local/ufg/build/draco-1.3.5/log.txt
```
