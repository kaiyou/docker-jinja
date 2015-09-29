FROM python:3

RUN pip install docker-py

ADD run.py /

VOLUMES ["/docker.sock", "/src", "/dst"]

CMD ["/run.py", "/docker.sock", "/src", "/dst"]
