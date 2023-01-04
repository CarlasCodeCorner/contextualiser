# get docker image
FROM python:3.8-slim-buster

# install requirements
COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt

# copy code
RUN mkdir app
WORKDIR /app
COPY main_langdetect.py /app/main_langdetect.py
COPY ./langdetect_service/ /app/langdetect_service/

ENV TOPIC=lang_detect
ENV MQ_HOST=rabbitmq

ENTRYPOINT ["python3","-u", "main_langdetect.py"]
