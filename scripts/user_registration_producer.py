

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
