import Adafruit_DHT
from picamera import PiCamera
import RPi.GPIO as GPIO
import base64
import datetime
import json
import math
import paho.mqtt.publish as publish
import time


MQTT_SERVER = "localhost"			# MQTT Broker IP Address
MQTT_PATH = "cs3103_group2_channel"	# Channel Name
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
DEBUG = True


def convertImageToBase64(image_filename):
	try:
		with open(image_filename, 'rb') as image_file:
			encoded = base64.b64encode(image_file.read()).decode("utf-8")
		return encoded
	except:
		print("Failed to encode camera image.")


def takeSnapshot(camera):
	try:
		image_filename = './images/%s.jpg' % (datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'),)
		camera.capture(image_filename)
		return image_filename
	except:
		print("Failed to capture image on camera.")


def publish_pir_data(image_filename, image_base64):
	data = {"topic": "pir", "index": 1, "location": "Living Room", "datetime": datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'), 
		"image_filename": image_filename, "image_base64": image_base64}
	data_out = json.dumps(data)
	publish.single(MQTT_PATH, data_out, hostname=MQTT_SERVER)


def publish_dht11_data(humidity, temperature, image_filename, image_base64):
	data = {"topic": "dht11", "index": 1, "location": "Kitchen", "datetime": datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'), 
		"humidity": "{0:0.1f}%".format(humidity), "temperature": "{1:0.1f}C".format(temperature), 
		"image_filename": image_filename, "image_base64": image_base64}
	data_out = json.dumps(data)
	publish.single(MQTT_PATH, data_out, hostname=MQTT_SERVER)
		

if __name__ == "__main__":
	# Initial Setup
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	
	# Read output from HC-SR501 Infrared PIR Motion Sensor Module
	GPIO.setup(11, GPIO.IN)
	
	# Read output from Raspberry Pi Camera Module
	camera = PiCamera()
	camera.start_preview()
	
	while True:
		i = GPIO.input(11)
		if i == 0:			# When output from motion sensor is LOW
			time.sleep(1)
		elif i == 1:		# When output from motion sensor is HIGH
		
			# Alerts MQTT client when motion is detected (e.g. intruders in the house)
			image_filename = takeSnapshot(camera)
			image_base64 = convertImageToBase64(image_filename)		
			publish_pir_data(image_filename, image_base64)
			time.sleep(2)
			
			if DEBUG:
				print("Motion detected on PIR motion sensor.")
		
		# Read output from DHT11 Temperature & Humidity Sensor Module
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		
		if humidity is not None and temperature is not None:
		
			# Alerts MQTT client when an abnormally high temperature is detected (e.g. fire in the kitchen)
			if temperature > 40.0:
				image_filename = takeSnapshot(camera)
				image_base64 = convertImageToBase64(image_filename)	
				publish_dht11_data(humidity, temperature, image_filename, image_base64)
				
			if DEBUG:
				print("Humidity={0:0.1f}% Temp={1:0.1f}C".format(humidity, temperature))
			time.sleep(2)
			
		else:
			if DEBUG:
				print("DHT11 sensor failure. Check wiring.")
