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
