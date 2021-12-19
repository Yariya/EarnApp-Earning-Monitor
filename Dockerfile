FROM python:alpine
ENV PYTHONUNBUFFERED=1
ENV container=docker
COPY app /app
WORKDIR /app
RUN pip install pyEarnapp discord_webhook colorama
CMD [ "python","./main.py" ]
