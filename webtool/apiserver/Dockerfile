FROM python:3.6.9-slim

WORKDIR /home/app 

COPY ["*.py", "requirements.txt","./" ]
RUN mkdir tmp
COPY classifier ./classifier
RUN pip install -r requirements.txt

EXPOSE 3000 

CMD gunicorn --bind 0.0.0.0:3000 --keyfile /home/app/certs/server.key --certfile /home/app/certs/server.crt --ca-certs /home/app/certs/ca-crt.pem --cert-reqs 2  app:app