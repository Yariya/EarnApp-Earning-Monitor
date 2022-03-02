FROM python:slim
ENV PYTHONUNBUFFERED=1
ENV container=docker
WORKDIR /app
RUN pip install pyEarnapp discord_webhook colorama matplotlib
CMD [ "python","./main.py" ]
ARG CACHEBUST=0
COPY app /app
