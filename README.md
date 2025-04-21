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

### Verification: Docker, Docker Compose, Vim Installation & User Access


