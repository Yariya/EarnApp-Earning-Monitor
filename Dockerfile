FROM python:3.6-alpine
ENV PYTHONUNBUFFERED=1
ENV container=docker
COPY app /app
WORKDIR /app
RUN apk add g++ jpeg-dev zlib-dev libjpeg make
RUN pip install pyEarnapp discord_webhook colorama matplotlib
CMD [ "python","./main.py" ]
