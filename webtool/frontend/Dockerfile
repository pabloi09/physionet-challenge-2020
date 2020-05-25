FROM node:12.15.0-alpine

WORKDIR /home/node/app
COPY ["package.json", "package-lock.json*","./" ]
COPY src ./src
COPY public ./public
RUN npm install
RUN npm run build

EXPOSE 5000

CMD npx serve -s build