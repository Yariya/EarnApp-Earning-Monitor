FROM python:alpine
ENV PYTHONUNBUFFERED=1
COPY app /app
WORKDIR /app
RUN pip install requests discord_webhook
CMD [ "python","./main.py" ]