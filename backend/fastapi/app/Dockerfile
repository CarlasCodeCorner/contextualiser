# get docker image
FROM python:3.8-slim-buster

# install requirements
COPY requirements.txt /
RUN pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

# copy code
RUN mkdir -p app/{models,router,services,dependencies}
#WORKDIR /app
COPY server.py /app/server.py

COPY routers/  /app/routers/
COPY models/  /app/models/
COPY services/  /app/services/
COPY dependencies/  /app/dependencies/

COPY pika_connector.py /app/pika_connector.py
COPY central_utils.py /app/central_utils.py

ENV MQ_HOST=rabbitmq
ENV MONGO_HOST=localhost
ENV ELASTICSEARCH_URL=https://elasticsearch:9200/

EXPOSE 8000

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]

