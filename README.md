## Project Overview
Real-Time Telecom is a system designed to process, store, and visualize telecom user activity in real time. It leverages Kafka for data streaming, PostgreSQL for data storage, and Streamlit for interactive dashboards. The project also includes a FastAPI backend for API-based data access.

## Architecture
The project consists of the following components:
- **Kafka Consumer**: Processes user activity data from Kafka topics and stores it in PostgreSQL.
- **PostgreSQL Database**: Stores user activity logs with conflict resolution for updates.
- **FastAPI Backend**: Provides RESTful APIs for accessing user activity data.
- **Streamlit Dashboard**: Visualizes real-time data with interactive maps and metrics.
- **Python**: Implements data processing, Kafka integration, database operations, API, and dashboard.

(Please ignore the fact that I changed the theme and wallpaper in some parts — it's still the same desktop environment.)


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


## But after working several times on the virtual machine on my laptop, it started to slow down because Kafka and other components require decent resources. So I ended up installing everything directly on my laptop, skipping the VM for convenience.

## I switched to Linux Ubuntu directly on my laptop instead of using it in a virtual machine.

![Screenshot from 2025-05-03 19-52-26](https://github.com/user-attachments/assets/393380ab-2bc1-4e03-b65a-86accdf5ae61)




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

![Screenshot from 2025-05-03 20-11-03](https://github.com/user-attachments/assets/cb947bb4-a58c-4a9b-ba43-2585421a0986)

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

![Screenshot from 2025-05-03 20-12-58](https://github.com/user-attachments/assets/205d8963-1118-4fd5-a3a5-0c46bad5f45f)

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
![Screenshot from 2025-05-03 20-14-19](https://github.com/user-attachments/assets/8f7e6401-343b-4771-8e6d-dd8368b9bf6a)


2. Now let's run the Docker Compose command using the file we created to start the PostgreSQL container on port 5432 (5432 the default port for PostgreSQL databases).

```bash

docker-compose -f docker-compose/postgres.yml up -d

then the container status and its condition are checked:

docker ps --filter "name=postgres"

docker inspect -f '{{.State.Status}}' postgres
(I find it convenient to use filters with Docker commands because I want to target specific containers)
```

![Screenshot from 2025-05-03 20-16-27](https://github.com/user-attachments/assets/6bc9c336-0ed9-49e1-a961-da2940b0cbff)


Before accessing the PostgreSQL database and running the psql command, you need to install the client that allows you to create a database and execute PostgreSQL SQL commands.
![Screenshot from 2025-05-03 19-03-18](https://github.com/user-attachments/assets/896829d6-9a96-4089-a11f-c16b44008916)

![Screenshot from 2025-05-03 19-07-17](https://github.com/user-attachments/assets/7aadc418-eeb3-4541-9d62-e3f876b22af9)



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
![Screenshot from 2025-05-03 20-21-07](https://github.com/user-attachments/assets/ae850f69-8b9f-408a-a234-0a4a7989a292)


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
![Screenshot from 2025-05-03 20-32-12](https://github.com/user-attachments/assets/4e8deed9-5046-4023-b9b6-c6d469576523)

Please ignore the other topics — they were created during earlier test runs.

5. Produce & Consume Messages

Start a producer in kafka container:

```bash

Start a producer:

kafka-console-producer --topic test-topic-1 --bootstrap-server localhost:9092

Start a consumer (in a second terminal):

kafka-console-consumer --topic test-topic-1 --bootstrap-server localhost:9092 --from-beginning

```
![output1](https://github.com/user-attachments/assets/d44fdca9-cc34-41f0-a35a-d9f7cb6d62f5)

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

![Screenshot from 2025-05-03 21-02-02](https://github.com/user-attachments/assets/7afffe86-e097-46e5-a590-e7f56177fa7d)

I won’t walk through the installation of each individual library step by step. Instead, here is a list of all required packages that you can install in one command using pip:


```bash

pip install kafka-python psycopg2 pandas requests

```
## Navigate to scripts/ and Create the First Python Producer
Now let's move into the scripts/ directory and create our first Python script. This script will simulate user registrations for a telecom company and send the generated data to a Kafka topic named user-registration.


```bash

cd ~/devops-data-city/scripts

Create a Python file:

vim user_producer.py

and add this code

```

```python


from kafka import KafkaProducer
from faker import Faker
import json
import random
import time
from datetime import datetime


fake = Faker()

#Configure Kafka producer with the appropriate settings
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  #Brokker Address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

#Define possible values for user attributes
genders = ['Male', 'Female']
devices = ['iPhone 13', 'Samsung S22', 'Xiaomi Redmi Note 11', 'OnePlus 10', 'Google Pixel 7']
tariffs = ['Unlimited Max', 'Basic 5GB', 'Night Surfer', 'Weekend Plan', 'Student Pack']
statuses = ['active', 'pending', 'inactive']

#Generate and send 20 user registration events
for user_id in range(1, 21):
    #Randomly select gender and generate a name based on the gender
    gender = random.choice(genders)
    name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()

    #Create a dictionary with user data
    user_data = {
        "user_id": user_id,
        "name": name,
        "age": random.randint(18, 65),
        "gender": gender,
        "state": fake.state(),
        "city": fake.city(),
        "device": random.choice(devices),
        "tariff": random.choice(tariffs),
        "connection_date": datetime.now().strftime("%Y-%m-%d"),
        "balance_usd": round(random.uniform(0, 100), 2),
        "status": random.choice(statuses)
    }

    #Send the user data to the Kafka topic 'user-registration'
    producer.send('user-registration', value=user_data)
    print(f"[✔] Sent: {user_data}")

    time.sleep(1)

#Ensure all messages are sent before exiting
producer.flush()
#print("All 20 users successfully sent.")

```

This script does the following:
- Generates fake telecom user data using the Faker library
- Sends 20 unique user registration events to the Kafka topic user-registration
- Uses the kafka-python library to handle Kafka message production
- Waits 1 second between messages to simulate real-time user onboarding
- Flushes the producer at the end to ensure all messages are delivered

![Screenshot from 2025-05-03 21-19-58](https://github.com/user-attachments/assets/cb2a703f-4cd9-4cf7-8c94-4745b9b73e1f)


After running the user_registration_producer.py script, synthetic user registration data was successfully generated and sent to the Kafka topic named user-registration. Each record represents a unique user with attributes like name, age, gender, location, device, tariff, balance, and connection status.

You can now verify the messages were published to the topic using Kafka's console consumer tool. (I stopped the code myself so that all IDs up to 20 would not be created)

![output2](https://github.com/user-attachments/assets/d03ecd51-eb72-4afa-bb5a-38761371671f)

After running the Python Kafka producer, we can see that messages were successfully published to the topic user-registration. This is confirmed by using the kafka-console-consumer command from within the Kafka Docker container — we see the exact JSON messages sent from the producer.

![Screenshot from 2025-05-04 18-11-02](https://github.com/user-attachments/assets/d7a3097d-42b3-4cc2-8d45-5aaa47e8bd72)

Error: Consumer group 'user-registration-group' does not exist.

This happens because no consumer has yet subscribed to the topic using that group ID. Kafka only tracks lag and offsets after a consumer with the specified group.id actually connects and starts reading messages (and commits offsets).

Next step: write and run a Kafka consumer in Python with group_id='user-registration-group' so that Kafka starts tracking this group and we can then monitor offsets and lag.

## Now let's write a consumer that will read from the producer and write to the PostgreSQL database I deployed in a Docker container.


```bash
from kafka import KafkaConsumer
import json
import psycopg2
from psycopg2 import OperationalError, IntegrityError

#Connection to PostgreSQL
conn = psycopg2.connect(
    dbname='demo',
    user='dev',
    password='dev123',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

#Create table with unique user_id
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_registration_log (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    state TEXT,
    city TEXT,
    device TEXT,
    tariff TEXT,
    connection_date DATE,
    balance_usd NUMERIC,
    status TEXT
)
""")
conn.commit()

#Kafka Consumer
consumer = KafkaConsumer(
    'user-registration',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='user-registration-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening to Kafka. Updating or inserting data by user_id.")

for message in consumer:
    user_data = message.value
    print(f"Received: {user_data}")

    try:
        cursor.execute("""
            INSERT INTO user_registration_log (
                user_id, name, age, gender, state, city, device,
                tariff, connection_date, balance_usd, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                name = EXCLUDED.name,
                age = EXCLUDED.age,
                gender = EXCLUDED.gender,
                state = EXCLUDED.state,
                city = EXCLUDED.city,
                device = EXCLUDED.device,
                tariff = EXCLUDED.tariff,
                connection_date = EXCLUDED.connection_date,
                balance_usd = EXCLUDED.balance_usd,
                status = EXCLUDED.status
        """, (
            user_data["user_id"],
            user_data["name"],
            user_data["age"],
            user_data["gender"],
            user_data["state"],
            user_data["city"],
            user_data["device"],
            user_data["tariff"],
            user_data["connection_date"],
            user_data["balance_usd"],
            user_data["status"]
        ))

        conn.commit()
        consumer.commit()
        print("Data recorded/updated. Offset committed.")

    except (OperationalError, IntegrityError) as e:
        conn.rollback()
        print(f"Error writing to PostgreSQL: {e}. Offset NOT committed.")


```

![Screenshot from 2025-05-04 18-43-58](https://github.com/user-attachments/assets/39688d7c-7389-4377-9a4f-883834519554)

Running the consumer code will read messages from the topic and write them to the PostgreSQL database.

![output4](https://github.com/user-attachments/assets/d2ca110d-c825-4b83-b8c2-fff40cda921b)


