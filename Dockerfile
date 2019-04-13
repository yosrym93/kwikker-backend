FROM ubuntu

WORKDIR '/app'


RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
EXPOSE 5000
CMD python3 run.py --env=production