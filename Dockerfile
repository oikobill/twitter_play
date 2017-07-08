FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get install -y sqlite3 libsqlite3-dev
ENTRYPOINT ["python"]
CMD ["app.py"]

