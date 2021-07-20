FROM python:3.9
WORKDIR /app

COPY compose/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ../.. .