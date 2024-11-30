from gpiozero import MCP3008
from time import sleep
from kafka import KafkaProducer
import spidev
import json
import flask from FLask, request, jsonify

# Create instance of FLask application, allowing to define routes and handle HTTP requests
app = Flask(__name__)

# Define the topic name, and Kafka broker address
KAFKA_TOPIC = "plant_data"
KAFKA_BROKER = "localhost:9092"

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER], 
        value_serializer=lambda v: json.dumps(v).encode('utf-8')) #Serialize JSON messages

@app.route('/send-moisture', methods=['POST'])
def kafkaProducer():


def moistureCalculation():
        #Define the channel for the moisture sensor
        moisture_channel = MCP3008(channel=0)

        #Threshold values for dry vs wet (adjust based on your testing)
        DRY_THRESHOLD = 0.75 #High value for dry condition, to be adjusted as needed (between 0 and 1)
        WET_THRESHOLD = 0.35 #Lower value for wet condition, to be adjusted as needed (between 0 and 1)

        while True:
                #Read analog value from the moisture sensor
                moisture_value = moisture_channel.value
                        
                #Check moisture level and detgermine if plant needs watering
                if moisture_value >= DRY_THRESHOLD:
                        print("Moisture Level: Dry! Plant needs watering.")
                elif moisture_value <= WET_THRESHOLD:
                        print("MOisture Level: Wet! No need for watering.")
                else:
                        print("Moisture Level: Moderate")
                
                #Print raw values for reference
                print(f"Moisture Sensor Value: {moisture_value:.2f}\n")
                
                #Delay to avoid excessive readings
                sleep(10)


__init__ main():
        
