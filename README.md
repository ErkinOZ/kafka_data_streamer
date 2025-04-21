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


and Run a Test Query to Verify

SELECT version();

Bonus: Create a test table (optional):

CREATE TABLE test_table (id SERIAL PRIMARY KEY, name TEXT);
INSERT INTO test_table (name) VALUES ('Kafka Test');

SELECT * FROM test_table;

```

![Screenshot from 2025-04-20 22-03-40](https://github.com/user-attachments/assets/f6ed2195-866b-40ef-add9-9fa407c961ac)

As we can see, the PostgreSQL database has been successfully deployed in a Docker container using a YAML file, and psql commands are working as expected.


## Kafka Service Definition


Create the Kafka YAML File, Start Kafka and Zookeeper with Docker Compose, Verify Container Status

1. Create a yaml file and write it to the /docker-compose directory:




```yaml
version: "3.8"

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.2   # Official Zookeeper image from Confluent
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181           # Port to connect to Zookeeper
      ZOOKEEPER_TICK_TIME: 2000             # Basic time unit in milliseconds used by Zookeeper
    ports:
      - "2181:2181"                         # Expose port 2181 for external access

  kafka:
    image: confluentinc/cp-kafka:7.3.2      # Official Kafka image from Confluent
    container_name: kafka
    depends_on:
      - zookeeper                           # Kafka depends on Zookeeper service
    ports:
      - "9092:9092"                         # Expose Kafka port for external access
    environment:
      KAFKA_BROKER_ID: 1                    # Unique ID for the Kafka broker
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181  # Address of the Zookeeper instance
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092  # External address for clients to connect
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT  # Map listener names to security protocols
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1   # Number of replicas for internal Kafka topics like offsets

```
2. Start Kafka and Zookeeper with Docker Compose

```bash

docker-compose -f docker-compose/kafka.yml up -d

```

3. Verify Container Status
 
```bash

docker ps --filter "name=kafka"
docker ps --filter "name=zookeeper"

docker inspect -f '{{.State.Status}}' kafka
docker inspect -f '{{.State.Status}}' zookeeper

docker logs kafka
docker logs zookeeper

```
4. Basic Kafka Commands (inside the container)

```bash

Enter Kafka container:

docker exec -it kafka bash

Create a topic:

kafka-topics --create --topic test-topic-1 --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

List topics:

kafka-topics --list --bootstrap-server localhost:9092

Describe a topic:

kafka-topics --describe --topic test-topic-1 --bootstrap-server localhost:9092

```
![Screenshot from 2025-04-20 22-18-38](https://github.com/user-attachments/assets/97cbfeac-7527-45b0-83d1-833d75be4773)

Please ignore the other topics — they were created during earlier test runs.

5. Produce & Consume Messages

Start a producer in kafka container:

```bash

Start a producer:

kafka-console-producer --topic test-topic-1 --bootstrap-server localhost:9092

Start a consumer (in a second terminal):

kafka-console-consumer --topic test-topic-1 --bootstrap-server localhost:9092 --from-beginning

```
![Screenshot from 2025-04-20 22-26-48](https://github.com/user-attachments/assets/b6f402fd-87a1-4d9a-825a-6c515fd52cde)

As you can see, Kafka is actively running and functioning correctly on the test topic.

What Are Topics, Producers, and Consumers?

Topic:
A topic in Kafka is a named channel where data is published. Think of it as a logical stream or category for messages. Producers write messages to a topic, and consumers read messages from it.

Producer:
A producer is a client or service that sends (publishes) data to Kafka topics. It could be anything — a microservice, an IoT device, or a data pipeline writing events to Kafka.

Consumer:
A consumer is a client or service that subscribes to topics and reads data from them. It processes or stores the data, depending on the use case (e.g., logging, analytics, storage, etc.).

## Set Up Python Virtual Environment (Before We Work in scripts/)

Before we move into the scripts/ folder where we’ll write Python files containing the core logic for handling telecom client data, we need to set up a clean Python virtual environment. This ensures that all dependencies are isolated and won’t affect the global system environment.

```bash

cd ~/devops-data-city

python3 -m venv venv

```
This creates a folder named venv that contains a standalone Python environment.

Activate the Virtual Environment

```bash

source venv/bin/activate

```

![Screenshot from 2025-04-20 22-56-23](https://github.com/user-attachments/assets/1aa8ee49-9027-46b9-9586-7f280fea8e07)

I won’t walk through the installation of each individual library step by step. Instead, here is a list of all required packages that you can install in one command using pip:


```bash

pip install kafka-python psycopg2 pandas requests

```

After installing the packages, you can save the full list of installed libraries into a requirements.txt file using the command below:

```bash

pip freeze > requirements.txt

```
This allows you to easily reproduce the environment later or share it with others using:

```bash

pip install -r requirements.txt

```
![Screenshot from 2025-04-20 23-02-06](https://github.com/user-attachments/assets/7a174bfb-5586-4ec9-abd5-2f71645b878c)

