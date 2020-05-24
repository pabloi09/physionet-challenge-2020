FROM python:3.6.9-slim

WORKDIR /home/app 

COPY ["*.py", "requirements.txt","./" ]
COPY tmp ./tmp
COPY classifier ./classifier
RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host 0.0.0.0

