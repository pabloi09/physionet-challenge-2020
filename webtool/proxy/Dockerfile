FROM nginx:1.18.0-alpine

RUN rm /etc/nginx/conf.d/default.conf 
WORKDIR /etc/nginx/conf.d
COPY ["default.conf","./" ]
RUN mkdir /etc/letsencrypt