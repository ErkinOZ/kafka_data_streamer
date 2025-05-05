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
