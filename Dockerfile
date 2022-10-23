FROM python:3.8-slim-buster

COPY . /app
#COPY requirements.txt .

WORKDIR /app
#RUN pip install -r requirements.txt

RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt')"

COPY /root/nltk_data/ /app/nltk_data

EXPOSE $PORT

#CMD ["flask", "run", "--bind 0.0.0.0:$PORT"]
#CMD flask run --bind 0.0.0.0:$PORT - no such bind
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
#CMD flask run gunicorn --workers=4 --bind 0.0.0.0:$PORT
#CMD run --bind 0.0.0.0:$PORT app:app