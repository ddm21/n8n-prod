# n8n-prod

### ✅ Download Script using wget:
```
wget https://gitlab.com/bmcgonag/docker_installs/-/raw/main/install_docker_nproxyman.sh
```
### ✅ Change Script Permission:
```
chmod +x install_docker_nproxyman.sh
```
### ✅ Now we can run the script with the command:
```
./install_docker_nproxyman.sh
```

### ✅ To start it execute:
```
docker-compose up -d
```

### ✅ To stop it execute:
```
docker-compose stop
```

### ✅ Run this command to list all running containers, including your n8n-worker instances:
```
docker ps --filter "name=n8n-worker"
```

### ✅ To increase the number of workers dynamically, use the scale command:
```
docker-compose up --scale n8n-worker=2 -d
```

### ✅ If you've made changes in docker-compose and want to restart while scaling workers, use:
```
docker-compose up --scale n8n-worker=2 --force-recreate -d
```
