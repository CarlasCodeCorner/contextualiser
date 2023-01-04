FROM mongo:latest
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=admin
ENV MONGO_INITDB_DATABASE=contextualiser

COPY mongo-init.js /docker-entrypoint-initdb.d/
RUN chmod  777 -R /data

RUN apt-get update
RUN apt-get install -y mongodb-org-shell
