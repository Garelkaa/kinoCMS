FROM python:3.12

ENV PYTHONPATH /usr/src/kinoCMS

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static

WORKDIR $PYTHONPATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Додайте цей рядок, щоб Django додаток експортував порт 8000

RUN chmod -R 755 /usr/src/kinoCMS/static/

RUN apt-get update && apt-get install --no-install-recommends -y \
  # Залежності для збірки Python-пакетів
  build-essential \
  # Залежності для psycopg2
  libpq-dev \
  # curl
  curl \
  # add ffmpeg
  ffmpeg

COPY . $PYTHONPATH
COPY ./requirements.txt $PYTHONPATH
RUN pip install -r requirements.txt
