FROM nginx:1.18.0-alpine

RUN mkdir /etc/nginx/sites-available
RUN mkdir /etc/nginx/sites-enabled
RUN rm /etc/nginx/conf.d/default.conf 
WORKDIR /etc/nginx/sites-available
COPY ["app.nginx","./" ]
RUN ln -s /etc/nginx/sites-available/app.nginx /etc/nginx/sites-enabled/app.nginx
RUN mkdir /etc/letsencrypt