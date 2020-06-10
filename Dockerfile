FROM python:3.8.2
ADD . /code
WORKDIR /code
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y libevent-dev
RUN apt-get install -y libgdal-dev
RUN apt-get install -y gdal-bin
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]