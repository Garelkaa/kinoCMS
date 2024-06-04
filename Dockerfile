FROM python:3.12

ENV PYTHONPATH /usr/src/kinoCMS

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static

WORKDIR $PYTHONPATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add this line to export port 8000 for Django app

RUN chmod -R 755 /usr/src/kinoCMS/static/


RUN apt-get update && apt-get install --no-install-recommends -y \
  # Dependencies for building Python packages
  build-essential \
  # Dependencies for psycopg2
  libpq-dev \
  # curl
  curl \
  # add ffmpeg
  ffmpeg

COPY . $PYTHONPATH
COPY ./requirements.txt $PYTHONPATH/

RUN pip install -r requirements.txt
