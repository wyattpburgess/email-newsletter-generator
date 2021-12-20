FROM python:3.6

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

WORKDIR /project

ADD . /project

RUN pip install -r requirements.txt

CMD ["python","run.py"]