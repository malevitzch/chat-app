FROM python:slim-buster

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt update && apt install -y sqlite3

COPY ./flask/. /var/api/

EXPOSE 8000
WORKDIR /var/api/
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "4"]
