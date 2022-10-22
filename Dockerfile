FROM python:3.8-slim-buster

# COPY . /app
COPY requirements.txt .

# WORKDIR /app
RUN pip install -r requirements.txt

# RUN pip install -r requirements.txt
COPY . .

EXPOSE $PORT

CMD ["python3", "app_flask.py", "run", "--bind 0.0.0.0:$PORT"]