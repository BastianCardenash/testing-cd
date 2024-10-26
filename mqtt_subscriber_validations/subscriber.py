from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import json
import os
import requests
from time import sleep

load_dotenv()

# MQTT Settings
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_TOPIC = 'fixtures/validation'
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

# REST API Endpoint
#API_URL = "http://django:8000/api/requests/validation/"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker! (Result code: {rc})")
    if rc != 0:
        print("Failed to connect, return code %d\n", rc)
    else:
        client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    
    try:
        # Solucion temporal para asegurarse de que se cree el request antes de validarlo.
        request_id = data['request_id']
        API_URL = f"http://django:8000/api/requests/validation/{request_id}/"
        response = requests.patch(API_URL, json=data)
        if response.status_code == 200:
            print(f"Validated request successfully.")
        else:
            print(f"Failed to validate request: {response.content}")

    except Exception as e:
        print(f"Failed to process message: {e}")

client = mqtt.Client()
client.enable_logger()

# Set MQTT username and password
print(MQTT_USERNAME, MQTT_PASSWORD)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

print(client.username, client.password)
client.connect(MQTT_HOST, MQTT_PORT, 60)

client.loop_forever()