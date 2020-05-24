FROM python:3.6.9-slim

WORKDIR /home/app
COPY build ./build
COPY ["*.py", "requirements.txt", "*.pem" ,"./" ]
RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn --certfile=certificate.pem --keyfile=key.pem -b 0.0.0.0:5000 app:app





