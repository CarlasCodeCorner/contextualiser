# get docker image
FROM python:3.8-slim-buster

# install requirements
COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt

# copy code
RUN mkdir -p app/{query_services,models}
WORKDIR /app
COPY main_query.py /app/main_connect.py

COPY query_services/ /app/query_services/

COPY models/ /app/models/

ENV TOPIC=connect

ENTRYPOINT ["python3", "main_connect.py"]