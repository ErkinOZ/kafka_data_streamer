## Project Overview
Real-Time Telecom is a system designed to process, store, and visualize telecom user activity in real time. It leverages Kafka for data streaming, PostgreSQL for data storage, and Streamlit for interactive dashboards. The project also includes a FastAPI backend for API-based data access.

## Architecture
The project consists of the following components:
- **Kafka Consumer**: Processes user activity data from Kafka topics and stores it in PostgreSQL.
- **PostgreSQL Database**: Stores user activity logs with conflict resolution for updates.
- **FastAPI Backend**: Provides RESTful APIs for accessing user activity data.
- **Streamlit Dashboard**: Visualizes real-time data with interactive maps and metrics.
- **Python**: Implements data processing, Kafka integration, database operations, API, and dashboard.

## Set up a virtual machine with Ubuntu Linux 20.04 using Oracle VirtualBox

![Снимок экрана 2025-04-20 204035](https://github.com/user-attachments/assets/313cde04-e4a0-4597-a030-5c6e13e50e56)

Checking versions and the status of the virtual machine on Linux:
```bash
   cat /etc/os-release
```

![Screenshot from 2025-04-20 20-45-45](https://github.com/user-attachments/assets/98407359-4117-43b6-b667-c07c8e574ffc)

Checked VM health/status(By default, only top is available. You can install htop using the following command: sudo apt update && sudo apt install htop -y
):

```bash
   htop
```
![Screenshot from 2025-04-20 20-50-36](https://github.com/user-attachments/assets/f9dbea89-b666-45ac-a2b6-4b20aa04e7aa)

## Install Docker, Docker Compose, Grant User Permissions & Set Up Vim
---

## 1. Install Docker

```bash
sudo apt update
sudo apt install -y docker.io

sudo systemctl enable docker
sudo systemctl start docker
```

## 2. Add Your User to Docker Group

```bash

sudo usermod -aG docker $USER

newgrp docker

```


## 3. Install Docker Compose
```bash

From APT:

sudo apt install -y docker-compose

or Latest version from GitHub:

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose


```

## 4. Install Vim (because "nano" is not convenient for me)
```bash

sudo apt install -y vim

```
## 5. Verification: Docker, Docker Compose, Vim Installation & User Access


```bash

docker --version

and Check Docker Service Status:

sudo systemctl status docker

and Verify that the user is in the docker group:

groups

```
![Screenshot from 2025-04-20 21-10-15](https://github.com/user-attachments/assets/f42479ba-8b02-44e5-8e84-4498e9d53aad)
![Screenshot from 2025-04-20 21-15-40](https://github.com/user-attachments/assets/8da2983c-469e-4de0-ab06-f3dd7ceb8a15)

I won't include basic checks like verifying the Vim version, but we did confirm that Docker is installed and running properly, and that the user is in the docker group with access to run Docker commands.

## Create Project Directory Structure

```bash

mkdir -p ~/devops-data-city/{docker-compose,scripts}

```
1. scripts/
Purpose:
This folder contains all the Python scripts used in the project. It includes the logic for data processing, API creation, and dashboard visualization.

2. docker-compose/ (or docker-compose.yml)
Purpose:
This folder or file is used to define and manage the Docker containers required for the project. It simplifies the setup of services like Kafka, Zookeeper, and PostgreSQL.

![Screenshot from 2025-04-20 21-28-26](https://github.com/user-attachments/assets/e6a7bcca-9dc5-4bd3-8a3e-4def8c06609c)

## Deployed a PostgreSQL database using a YAML-based Docker Compose file to store data received from Kafka.

1. Create a yaml file and write it to the /docker-compose directory:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:15
    container_name: postgres
    restart: always
    environment:
      POSTGRES_DB: demo
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev123
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:

```
![Screenshot from 2025-04-20 21-41-58](https://github.com/user-attachments/assets/6ed59869-f679-4c97-b799-096ee8d850ed)

2. Now let's run the Docker Compose command using the file we created to start the PostgreSQL container on port 5432 (5432 the default port for PostgreSQL databases).

```bash

docker-compose -f docker-compose/postgres.yml up -d

then the container status and its condition are checked:

docker ps --filter "name=postgres"

docker inspect -f '{{.State.Status}}' postgres
(I find it convenient to use filters with Docker commands because I want to target specific containers)
```

![Screenshot from 2025-04-20 21-50-34](https://github.com/user-attachments/assets/aa69f49c-e28d-4bba-875e-3daf3268d6cf)

3. Once we confirm that the PostgreSQL Docker container is in a running state, it means the service has started successfully.
Now we can proceed to verify the PostgreSQL instance by connecting to it via psql and executing a simple SELECT query to ensure everything is working as expected.

```bash

psql -h localhost -U dev -d demo

-h localhost — connects to the PostgreSQL server running on your local machine

-U dev — uses the dev user to authenticate

-d demo — connects to the demo database

```



