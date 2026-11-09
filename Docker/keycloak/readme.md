# Securing apps with Keycloak

Example from https://authpractice.com/keycloak-sso-docker-compose

## Setup on Linux

```bash
sudo apt install docker.io

# Check that Docker is running
systemctl status docker.service
```

To solve this error:

```bash
$ docker ps
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```

run:

```bash
sudo usermod -aG docker $USER
```

and then logout and log back in again.

To install Docker compose (from https://docs.docker.com/compose/install/linux/)

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v5.6.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

docker compose version
```

Install Node.js using:

```bash
sudo apt install nodejs npm
```

## Running

```bash
docker compose up
```

Open Keycloak at http://localhost:8080/ and login as admin/admin to check it is running.

Setup Keycloak by running:

```bash
chmod u+x setup.sh
./setup.sh
```

Setup name resolution for the host `keycloak.local` on Linux:

```bash
sudo vim /etc/hosts
# Add the line:
# 127.0.0.1  localhost keycloak.local
```

Setup name resolution for the host `keycloak.local` on Windows:
- Press the Windows key
- Search for Notepad
- Right-click on Notepad and start as Administrator
- File -> Open -> `%WINDIR%\System32\drivers\etc\hosts`
- Add the line:

```
127.0.0.1  localhost keycloak.local
```

Navigate to http://localhost:3000 or http://localhost:3001

## Clean up

```bash
docker-compose down
```
