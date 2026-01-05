FROM python:3.14-slim-trixie

WORKDIR /home/python
ENV PYTHONUNBUFFERED=TRUE

RUN apt-get update -y && \
    apt-get install -y curl && \
    useradd -m python --uid 1000; \
    chown -R python:python /home/python

USER python
COPY --chown=python:python requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY --chown=python:python . .

CMD [ "python3", "backend.py" ]
