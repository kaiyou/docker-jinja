FROM python:3

RUN pip install docker-py Jinja2

ADD run.py utils.py /

VOLUME ["/docker.sock", "/src", "/dst"]

ENTRYPOINT ["/run.py", "unix:///docker.sock", "/src", "/dst", "-t", "start", "die"]
