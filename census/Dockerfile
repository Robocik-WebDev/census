FROM node:14

WORKDIR /app

COPY app/package*.json ./

RUN apt-get update && apt-get install -y build-essential netcat libpq-dev
RUN npm install -g nodemon
RUN npm install

