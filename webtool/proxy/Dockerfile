FROM nginx:1.18.0-alpine

WORKDIR /etc/nginx/sites-enabled
RUN rm default
WORKDIR /etc/nginx/sites-available
RUN rm default
COPY ["app.nginx","./" ]
RUN ln -s /etc/nginx/sites-available/app.nginx /etc/nginx/sites-enabled/app.nginx

WORKDIR /etc
COPY ["hosts","./" ]

RUN mkdir /etc/letsencrypt