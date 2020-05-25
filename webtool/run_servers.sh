sudo docker kill $(sudo docker ps -a -q)
sudo docker image rm --force $(sudo docker image ls -a -q)
sudo docker system prune
sudo docker-compose build
sudo docker-compose up
