sudo docker kill --force $(sudo docker ps -a -q)
sudo docker image rm --force $(sudo docker image ls -a -q)
sudo docker system prune
cd frontend
npm run build
cd ..
sudo docker-compose build
sudo docker-compose up
