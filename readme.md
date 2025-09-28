

# Сборка контейнера

```console
docker build --no-cache --squash -t python_2025_14 -f Dockerfile .
```

# Запуск контейнера

```console
docker run -v ~/PycharmProjects/python_2025_14:/src -p 80:80 -p 8089:8089 -it python_2025_14 /bin/bash
```


# В контейнере

## Предварительно

```console
uv lock
uv sync
```

## В одном терминале запускаем наш сервер

```console
uv run server.py
```

На хост машине сервер доступен на http://localhost:80

Для тестирования HEAD и GET - http://localhost:80/test

## В другом терминале lucust

```console
uv run locust
```

На хост машине locust сервер доступен на http://localhost:8089 (там можно запускать нагрузочное тестирование)

