FROM python:3.7

MAINTAINER ukay

ARG DEBIAN_FRONTEND=noninteractive
    
COPY app /app

WORKDIR /app

RUN pip install --upgrade pip

RUN apt-get update 
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y

RUN apt-get install -y apt-utils

RUN pip install opencv-python

RUN apt-get install -y python-tk

RUN pip install -r requirements.txt

RUN pip install torch torchvision

CMD ["python", "app.py"]