FROM python:alpine
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt