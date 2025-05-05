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
