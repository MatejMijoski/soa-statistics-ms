FROM python:3.8

COPY ./migrations /workdir/migrations
COPY *.py /workdir/
COPY app.db /workdir/app.db
COPY ./requirements.txt /workdir/requirements.txt
COPY ./Repository /workdir/Repository
COPY ./Services /workdir/Services

WORKDIR /workdir

RUN pip install -r requirements.txt
EXPOSE 5000

CMD python app.py