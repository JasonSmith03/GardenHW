from kafka import KafkaConsumer
import json

# Kafka Config
KAFKA_TOPIC = "plant_data"
KAFKA_BROKER = "localhost:9092"

# Init Kafka Consumer
consumer = KafkaConsumer(
	KAFKA_TOPIC,
	bootstrap_servers=[KAFKA_BROKER],
	auto_offset_reset="earliest",
	enable_auto_commit=True,
	value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print(f"Listening to Kafka topic: {KAFKA_TOPIC}")

# Consume messages
for message in consumer:
	print(f"Received message: {message.value}")
