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

Let's check the PostgreSQL database — the data should be in the table.
![output5](https://github.com/user-attachments/assets/399f0e35-f44d-4480-b7f0-46bc42e24666)

In the table, we can see the messages that were generated by the Python code, received by the consumer, and written to the PostgreSQL database — here they are.

We also verified the table using DBeaver to ensure the data was correctly inserted.

![Screenshot from 2025-05-04 19-16-52](https://github.com/user-attachments/assets/827c4dc1-d90b-4de9-937b-db16eaaec554)

## Now let's write a Python script that will generate activity based on base stations, using the table we previously created and populated with data about registered users, including their state and other details. We'll first write a producer to send this activity data to a Kafka topic, and then a consumer to read from that topic and store the data in a PostgreSQL database.

Consumer: user_activity_producer.py
```bash

from kafka import KafkaProducer
import psycopg2
import json
import random
import time
from datetime import datetime
from faker import Faker

#Initialization
fake = Faker()

#Connecting to PostgreSQL to fetch user_id
conn = psycopg2.connect(
    dbname='demo',
    user='dev',
    password='dev123',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()
cursor.execute("SELECT user_id FROM user_registration_log")
user_ids = [row[0] for row in cursor.fetchall()]

if not user_ids:
    print("No users found in the user_registration_log table.")
    exit(1)

print(f"[✔] Retrieved {len(user_ids)} user_id(s) from PostgreSQL.")

#Configuring Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

#Possible activity parameters
basestations = [f"BS-{i}" for i in range(1, 6)]
hostnames = ['google.com', 'youtube.com', 'instagram.com', 'chat.openai.com', 'facebook.com']

#Generating activity in a loop
while True:
    user_id = random.choice(user_ids)
    lat, lng = float(fake.latitude()), float(fake.longitude())

    activity = {
        "user_id": user_id,
        "datetime": datetime.now().isoformat(),
        "basestation": random.choice(basestations),
        "hostname": random.choice(hostnames),
        "lat": lat,
        "long": lng
    }

    producer.send('user-activity', value=activity)
    print(f"Sent: {activity}")
    time.sleep(1)


```

Producer: user_activity_consumer.py
```bash

from kafka import KafkaConsumer
import json
import psycopg2
from psycopg2 import OperationalError, IntegrityError

#Connecting to PostgreSQL
conn = psycopg2.connect(
    dbname='demo',
    user='dev',
    password='dev123',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

#Creating the activity table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_activity_log (
    user_id INTEGER,
    datetime TIMESTAMP,
    basestation TEXT,
    hostname TEXT,
    lat DOUBLE PRECISION,
    long DOUBLE PRECISION,
    PRIMARY KEY (user_id, datetime)
)
""")
conn.commit()

#Configuring Kafka Consumer
consumer = KafkaConsumer(
    'user-activity',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='user-activity-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening to Kafka topic: user-activity.")

for message in consumer:
    activity = message.value
    print(f"Received: {activity}")

    try:
        cursor.execute("""
            INSERT INTO user_activity_log (
                user_id, datetime, basestation, hostname, lat, long
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, datetime) DO UPDATE SET
                basestation = EXCLUDED.basestation,
                hostname = EXCLUDED.hostname,
                lat = EXCLUDED.lat,
                long = EXCLUDED.long
        """, (
            activity["user_id"],
            activity["datetime"],
            activity["basestation"],
            activity["hostname"],
            activity["lat"],
            activity["long"]
        ))

        conn.commit()
        consumer.commit()
        print("Activity recorded/updated. Offset committed.")

    except (OperationalError, IntegrityError) as e:
        conn.rollback()
        print(f"Error writing to PostgreSQL: {e}. Offset NOT committed.")


```
## We created Python scripts for both the producer and the consumer to simulate user activity. Now we're running them together to demonstrate that they work simultaneously in a streaming setup.

![output6](https://github.com/user-attachments/assets/1008c7f0-a40d-44f0-b3f2-e5e4ad9af4ab)

The logs show that all messages were successfully consumed and written to PostgreSQL. Now let's check the PostgreSQL database to verify the data (I manually stopped the activity generation script myself)

Let's check the table directly using DBeaver by running a SELECT query.

![Screenshot from 2025-05-04 20-01-25](https://github.com/user-attachments/assets/16739d0b-7860-47f8-93f4-341f80e15602)

## Now we can join the user_registration_log table with the user_activity_log table using the user ID, so we get a complete picture of the registered users and their activity across base stations.

![Screenshot from 2025-05-04 20-05-32](https://github.com/user-attachments/assets/437c69b3-bdea-4043-adce-ea8bf6950184)

Joined user_registration_log and user_activity_log to display complete user activity details by base station, verified via DBeaver

## This service provides real-time monitoring of user activity based on data from PostgreSQL.

1) Listens to PostgreSQL tables user_registration_log and user_activity_log
2) Joins them by user_id
3) Displays data in real time as a dashboard (e.g., in Streamlit)
4) Continuously updates

Build a Streamlit app that:
1) Connects to PostgreSQL
2) Performs a JOIN between two tables every X seconds
3) Displays active users, activity by location, devices, domains, etc.
4) Runs in auto-refresh mode

! Run pip install streamlit inside your virtual environment !

```bash

pip install streamlit sqlalchemy

```
streamlit – for building interactive dashboards and web apps

sqlalchemy – for connecting to and querying databases

```bash

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# --------------------------
def get_engine():
    return create_engine('postgresql://dev:dev123@localhost:5432/demo')

# --------------------------
#Fetching joined data
# --------------------------
def fetch_joined_data():
    engine = get_engine()
    query = """
        SELECT 
            a.user_id,
            r.name,
            r.city,
            r.device,
            r.tariff,
            a.datetime,
            a.basestation,
            a.hostname,
            a.lat,
            a.long
        FROM user_activity_log a
        JOIN user_registration_log r ON a.user_id = r.user_id
        ORDER BY a.datetime DESC
        LIMIT 500
    """
    df = pd.read_sql(query, engine)
    return df

# --------------------------
# Streamlit settings
# --------------------------
st.set_page_config(page_title="User Activity Dashboard", layout="wide")
st.title("Real-Time Telecom User Activity")

# Fetching and preparing data
df = fetch_joined_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

df = df.rename(columns={"long": "longitude"})

#Metrics
st.subheader("General Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Unique Users", df["user_id"].nunique())
col2.metric("Base Stations", df["basestation"].nunique())
col3.metric("Domains", df["hostname"].nunique())

#General Activity Table
st.subheader("General Activity Table")
st.dataframe(df, use_container_width=True)

#Search by user_id
st.subheader("Search by User")
user_ids = sorted(df["user_id"].unique())
selected_user_id = st.selectbox("Select user_id", options=["All"] + user_ids)

#Filtered data by selected user_id
filtered_df = df if selected_user_id == "All" else df[df["user_id"] == selected_user_id]

#Activity Map
st.subheader("Activity Map")
if not filtered_df.empty:
    st.map(filtered_df[['lat', 'longitude']], use_container_width=True)
else:
    st.info("No activity for the selected user.")

#Additional Table for Selected User
st.subheader("Details for Selected user_id")
st.write(f"Records Found: **{len(filtered_df)}**")
st.dataframe(filtered_df, use_container_width=True)


```

Running the code:

![output7](https://github.com/user-attachments/assets/4764fc74-da9b-40e9-a610-b755f3d8e342)

After several tests and discussions with ChatGPT, I realized that querying PostgreSQL directly from Streamlit for real-time data is not efficient.

A better architectural solution is:

Streamlit should use FastAPI as a data source instead of connecting directly to PostgreSQL.

Why this is the right approach:
Clean separation of concerns: Streamlit handles the UI, FastAPI serves the data, PostgreSQL stores the data.

Reduced database load: FastAPI can cache or filter data before sending it to the frontend.

Improved security: No direct database access from the UI.

Reusability: FastAPI can serve other clients (mobile apps, other dashboards).

Scalability: FastAPI and Streamlit can be scaled independently.

## Creating the API (FastAPI)

1) db.py - Connecting to PostgreSQL

```bash

from sqlalchemy import create_engine

DATABASE_URL = "postgresql://dev:dev123@localhost:5432/demo"
engine = create_engine(DATABASE_URL)

```

2) crud.py — logic for retrieving data from the database


```bash

import pandas as pd
from db import engine

def get_all_activities(limit=500):
    query = f"""
        SELECT 
            a.user_id, r.name, r.city, r.device, r.tariff,
            a.datetime, a.basestation, a.hostname, a.lat, a.long
        FROM user_activity_log a
        JOIN user_registration_log r ON a.user_id = r.user_id
        ORDER BY a.datetime DESC
        LIMIT {limit}
    """
    return pd.read_sql(query, engine)

def get_activities_by_user(user_id: int):
    query = f"""
        SELECT 
            a.user_id, r.name, r.city, r.device, r.tariff,
            a.datetime, a.basestation, a.hostname, a.lat, a.long
        FROM user_activity_log a
        JOIN user_registration_log r ON a.user_id = r.user_id
        WHERE a.user_id = {user_id}
        ORDER BY a.datetime DESC
    """
    return pd.read_sql(query, engine)

def get_user_ids():
    query = "SELECT DISTINCT user_id FROM user_registration_log ORDER BY user_id"
    df = pd.read_sql(query, engine)
    return df["user_id"].tolist()


```

crud.py defines SQL queries to retrieve user activity data from PostgreSQL using pandas.

Uses JOIN to combine user_activity_log and user_registration_log

Executes SQL queries with pandas.read_sql()

Filters, sorts, and limits results directly in SQL for performance

3) main.py — FastAPI application
Defines the API endpoints that serve user activity data retrieved from the database via crud.py. It acts as the backend for the frontend dashboard (e.g., Streamlit).

```bash
from fastapi import FastAPI
from crud import get_all_activities, get_activities_by_user, get_user_ids

app = FastAPI()

@app.get("/")
def root():
    return {"message": "User Activity API is running"}

@app.get("/users")
def users():
    return {"users": get_user_ids()}

@app.get("/activities")
def activities():
    df = get_all_activities()
    return df.to_dict(orient="records")

@app.get("/activities/{user_id}")
def user_activity(user_id: int):
    df = get_activities_by_user(user_id)
    return df.to_dict(orient="records")


```
4) Running the app

```bash

uvicorn main:app --reload

```

![output8](https://github.com/user-attachments/assets/19bf6899-0e77-45c9-af51-f093ecd95b91)


http://localhost:8000/users – Get the list of all user IDs:
![Screenshot from 2025-05-04 20-55-09](https://github.com/user-attachments/assets/1412334e-f4cd-433c-8013-b1ecaa523433)
http://localhost:8000/activities – Get the latest 500 activity records:
![Screenshot from 2025-05-04 20-55-18](https://github.com/user-attachments/assets/15e152c1-fbda-49e9-a22f-74a065a991d0)
http://localhost:8000/activities/1 – Get all activity records for user ID 1:
![Screenshot from 2025-05-04 20-55-57](https://github.com/user-attachments/assets/fe571f2c-d4f6-4cb9-a556-71a8cfa2fbda)
http://localhost:8000/docs – Swagger UI (interactive API documentation):

