from gpiozero import MCP3008
from time import sleep
from kafka import KafkaProducer
import spidev
import json
import os
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

# Soil moisture sensor class
class SoilMoistureSensor:
        #Constructor
        def __init__(self, channel=0, dry_threshold=0.75, wet_threshold=0.55):
                try: 
                        self.moisture_channel = MCP3008(channel=channel)
                        print("MCP3008 init success.")
                except Exception as e:
                        print(f"Error in init MCP3008: {e}")
                self.dry_threshold = dry_threshold
                self.wet_threshold = wet_threshold
        
        def get_channel(self):
                return self.moisture_channel
        
        def get_moisture_value(self):
                return self.moisture_channel.value
        
        def get_moisture_status(self):
                #Determine the moisture level
                #Read analog value from the moisture sensor
                moisture_value = self.get_moisture_value()
                        
                #Check moisture level and detgermine if plant needs watering
                if moisture_value >= self.dry_threshold:
                        return "Moisture Level: Dry! Plant needs watering."
                elif moisture_value <= self.wet_threshold:
                        return "Moisture Level: Wet! No need for watering."
                else:
                        return "Moisture Level: Moderate"

# Kafka Producer class
class KafkaPublisher:
        # Constructor
        def __init__(self, topic, broker):
                self.topic = topic
                self.producer = KafkaProducer(bootstrap_servers=[broker], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        def send_data(self, data):
                # Send JSON data to the Kafka topic
                self.producer.send(self.topic, value=data)
                self.producer.flush()
                
# FLask Application
app = Flask(__name__)

# Kafka Config
KAFKA_TOPIC = "plant_data"
KAFKA_BROKER =  os.getenv("KAFKA_BROKER", "localhost:9092")

# Init classes
sensor = SoilMoistureSensor()
kafka_publisher = KafkaPublisher(topic=KAFKA_TOPIC, broker=KAFKA_BROKER)

# APScheduler
scheduler = BackgroundScheduler()

def publish_moisture_data():
        # Get current moisture data
        moisture_value = sensor.get_moisture_value()
        moisture_status = sensor.get_moisture_status()
        
        # Create JSON payload
        data = {
                "moisture_channel": 0,
                "name": "planty",
                "moisture_pct": round(moisture_value, 2),
                "status_msg": moisture_status,
        }
        
        # Publish to Kafka
        kafka_publisher.send_data(data)
        print(f"Published data: {data}")

# Schedule the task every 5 minutes
scheduler.add_job(publish_moisture_data, "interval", minutes=1)
scheduler.start()


@app.route("/send-moisture", methods=["POST"])
def send_moisture():
        # Get current moisture data
        moisture_value = sensor.get_moisture_value()
        moisture_status = sensor.get_moisture_status()
        moisture_channel = sensor.get_channel()
        
        # Create JSON payload
        data = {
                "moisture_channel": 0,
                "moisture_value": round(moisture_value, 2),
                "moisture_status": moisture_status,
        }
        
        # Publish to Kafka
        kafka_publisher.send_data(data)
        
        return jsonify({"status": "Message sent to Kafka", "data": data}), 200

if __name__ == "__main__":
        try:
                app.run(host="0.0.0.0", port=5000)
        except (KeyboardInterrupt, SystemExit):
                scheduler.shutdown()
