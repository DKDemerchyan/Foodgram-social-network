FROM python:3.8-slim

RUN mkdir /app

COPY . /app

RUN pip3 install -r /app/backend/foodgram/requirements.txt --no-cache-dir

WORKDIR /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]