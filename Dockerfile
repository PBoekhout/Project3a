FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN pip install --upgrade pip

ENV FLASK_APP=app.py

CMD ["python", "app.py"]
