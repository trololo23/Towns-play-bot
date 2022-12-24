FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.5

RUN apt-get install -y python3-pip

RUN pip install aiogram

RUN pip install redis

COPY . .
CMD ["python3", "bot.py"]