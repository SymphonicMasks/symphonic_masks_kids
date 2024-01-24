FROM ubuntu:latest
FROM node:20

WORKDIR /frontend/
# Install dependencies
COPY package.json .

RUN npm install


# Copy the current directory contents into the container at /app
COPY . .
WORKDIR /frontend/app
# Expose the port the app runs on
EXPOSE 3000

