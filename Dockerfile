FROM python:3.8-slim-buster

# COPY . /app
COPY requirements.txt .

# WORKDIR /app
RUN pip install -r requirements.txt

# RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python3", "app_flask.py", , "run", "--host=0.0.0.0", "--port=5000"]