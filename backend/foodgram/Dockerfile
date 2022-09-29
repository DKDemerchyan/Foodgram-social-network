FROM python:3.8-slim

WORKDIR /app

COPY . /app

RRUN pip3 install -r /app/backend/foodgram/requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]