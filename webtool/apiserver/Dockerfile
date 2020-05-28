FROM python:3.6.9-slim

WORKDIR /home/app 

COPY ["*.py", "requirements.txt","./" ]
RUN mkdir tmp
COPY classifier ./classifier
RUN pip install -r requirements.txt

EXPOSE 3000 

CMD gunicorn --bind 0.0.0.0:3000 app:app