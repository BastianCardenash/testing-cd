from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import json
import os
import requests

load_dotenv()

# MQTT Settings
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_TOPIC = 'fixtures/history'
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

# REST API Endpoint
API_URL = "http://django:8000/api/fixtures/history/create/batch"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker! (Result code: {rc})")
    if rc != 0:
        print("Failed to connect, return code %d\n", rc)
    else:
        client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}")
    data = json.loads(json.loads(msg.payload.decode()))
    
    try: 
        response = requests.post(API_URL, json=data)
        #API tiene que revisar el resultado y entregar la plata correctamente.
        if response.status_code == 201:
            print(f"Checked history successfully.")
        else:
            print(f"Failed to validate check history: {response.content}")

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