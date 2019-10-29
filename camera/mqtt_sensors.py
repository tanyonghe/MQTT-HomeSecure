import Adafruit_DHT
import RPi.GPIO as GPIO
import datetime
import json
import paho.mqtt.publish as publish
import time

import mqtt_camera


MQTT_SERVER = "localhost"			# MQTT Broker IP Address
MQTT_PATH = "cs3103_group2_channel"	# Channel Name
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
PACKET_SIZE = 3000
DEBUG = False


def publish_pir_data(image_filename, image_base64):
	data = {"topic": "pir", "index": 1, "location": "Living Room", "datetime": datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'), 
		"image_filename": image_filename, "image_base64": image_base64}
	data_out = json.dumps(data)
	publish.single(MQTT_PATH, data_out, hostname=MQTT_SERVER)
	#publishEncodedImage(snapshot_base64)

def publish_dht11_data(humidity, temperature, image_filename, image_base64):
	data = {"topic": "dht11", "index": 1, "location": "Kitchen", "datetime": datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'), 
		"humidity": "{0:0.1f}%".format(humidity), "temperature": "{1:0.1f}C".format(temperature), 
		"image_filename": image_filename, "image_base64": image_base64}
	data_out = json.dumps(data)
	#publish.single(MQTT_PATH, "DHT11 {0:0.1f}% {1:0.1f}C".format(humidity, temperature), hostname=MQTT_SERVER)
	publish.single(MQTT_PATH, data_out, hostname=MQTT_SERVER)
	#publishEncodedImage(snapshot_base64)
	
def publishEncodedImage(encoded):
 
	end = PACKET_SIZE
	start = 0
	length = len(encoded)
	picId = randomword(8)
	pos = 0
	no_of_packets = math.ceil(length/PACKET_SIZE)

 
	while start <= len(encoded):
		data = {"data": encoded[start:end], "pic_id": picId, "pos": pos, "size": no_of_packets}
		client.publishEvent("Image-Data", json.JSONEncoder().encode(data))
		end += PACKET_SIZE
		start += PACKET_SIZE
		pos = pos +1	

if __name__ == "__main__":
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(11, GPIO.IN)         			# Read output from HC-SR501 Infrared PIR Motion Sensor Module
	while True:
		i = GPIO.input(11)
		if i == 0:								# When output from motion sensor is LOW
			time.sleep(1)
		elif i == 1:							# When output from motion sensor is HIGH
			if DEBUG:
				print("Motion detected on PIR motion sensor!")
			image_filename = mqtt_camera.takeSnapshot()
			image_base64 = mqtt_camera.convertImageToBase64(image_filename)		
			publish_pir_data(image_filename, image_base64)	# Publish data to MQTT client
			time.sleep(1)
			
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)	# Read output from DHT11 Temperature & Humidity Sensor Module
		if humidity is not None and temperature is not None:
			if temperature > 40:												# If abnormally high temperature
				image_filename = mqtt_camera.takeSnapshot()
				image_base64 = mqtt_camera.convertImageToBase64(image_filename)	
				publish_dht11_data(humidity, temperature, image_filename, image_base64)	# Publish data to MQTT client
			if DEBUG:
				print("Humidity={0:0.1f}% Temp={1:0.1f}C".format(humidity, temperature))
		else:
			if DEBUG:
				print("Sensor failure. Check wiring.")