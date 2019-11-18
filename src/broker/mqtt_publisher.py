import Adafruit_DHT
import RPi.GPIO as GPIO
import base64
import datetime
import dropbox
from dropbox.exceptions import ApiError, AuthError
import json
import math
import os
import paho.mqtt.publish as publish
from picamera import PiCamera
import time
import smtplib
import subprocess
import sys


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


MQTT_SERVER = "localhost"			# MQTT Broker IP Address
MQTT_PATH = "cs3103_group2_channel"	# Channel Name
TLS_CERT_FILEPATH = ""	  		# TLS Certificate
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
DEBUG = True
MOTION = False
HIGHTEMP = False
DROPBOX_TOKEN = 'P-EM0zKgaQAAAAAAAAAADqTzlfXB5mSLqZOZ0D2fp-yqt1MruWWc5aJ_pTbUiYCw'


# Upload localfile to Dropbox
def uploadFile(localfile):

	# Check that access tocken added
	if (len(DROPBOX_TOKEN) == 0):
		sys.exit("ERROR: Missing access token. "
				 "try re-generating an access token from the app console at dropbox.com.")

	# Create instance of a Dropbox class, which can make requests to API
	print("Creating a Dropbox object...")
	dbx = dropbox.Dropbox(DROPBOX_TOKEN)

	# Check that the access token is valid
	try:
		dbx.users_get_current_account()
	except AuthError as err:
		sys.exit("ERROR: Invalid access token; try re-generating an "
				 "access token from the app console at dropbox.com.")
		
	uploadPath = '/videos' + localfile

	# Read in file and upload
	with open(localfile, 'rb') as f:
		print("Uploading " + localfile + " to Dropbox.")

		try:
			dbx.files_upload(f.read(), uploadPath)
		except ApiError as err:
			# Check user has enough Dropbox space quota
			if (err.error.is_path() and
					err.error.get_path().error.is_insufficient_space()):
				sys.exit("ERROR: Cannot upload; insufficient space.")
			elif err.user_message_text:
				print(err.user_message_text)
				sys.exit()
			else:
				print(err)
				sys.exit()

# Should securely store credentials but not our project focus
sender = 'cs3103test@gmail.com'
password = 'Password@123'
receiver = 'cs3103test2@gmail.com'


def send_mail(filename):
	print ('Sending E-Mail Notification')
	
	# Sending mail
	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receiver
	msg['Subject'] = 'Event Detected'
	
	body = 'Picture is Attached.'
	msg.attach(MIMEText(body, 'plain'))
	attachment = open(filename, 'rb')
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
	msg.attach(part)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(sender, password)
	text = msg.as_string()
	server.sendmail(sender, receiver, text)
	server.quit()


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
		

def takeVideo(camera):
	try:
		video_filename = './videos/%s.h264' % (datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'),)
		camera.start_recording(video_filename)
		time.sleep(10)
		camera.stop_recording()
		return video_filename
	except:
		print("Failed to capture video on camera.")


def publish_pir_data(index, image_filename, image_base64):
	data = {"topic": "pir", "index": index, "location": "Living Room", "datetime": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 
		"image_filename": image_filename, "image_base64": image_base64}
	data_out = json.dumps(data)

	if TLS_CERT_FILEPATH:
		publish.single(MQTT_PATH, data_out, tls={'ca_certs':TLS_CERT_FILEPATH}, port=8883, hostname=MQTT_SERVER, qos=1)
	else:
		publish.single(MQTT_PATH, data_out, hostname=MQTT_SERVER, qos=1)


def publish_dht11_data(index, humidity, temperature, image_filename, image_base64):
	data = {"topic": "dht11", "index": index, "location": "Kitchen", "datetime": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 
		"humidity": "{0:0.1f}%".format(humidity), "temperature": "{1:0.1f}C".format(temperature), 
		"image_filename": image_filename, "image_base64": image_base64}
	data_out = json.dumps(data)

	if TLS_CERT_FILEPATH:
		publish.single(MQTT_PATH, data_out, tls={'ca_certs':TLS_CERT_FILEPATH}, port=8883, hostname=MQTT_SERVER, qos=1)
	else:
		publish.single(MQTT_PATH, data_out, hostname=MQTT_SERVER, qos=1)
		

if __name__ == "__main__":
	# Initial Setup
	if not os.path.exists("./images"):
		os.mkdir("./images")
	elif not os.path.exists("./videos"):
		os.mkdir("./videos")

	index = 1
	
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
					if MOTION == False:
						MOTION = True
						image_filename = takeSnapshot(camera)
						image_base64 = convertImageToBase64(image_filename)
						publish_pir_data(index, image_filename, image_base64)
						video_filename = takeVideo(camera)
						uploadFile(video_filename)
						send_mail(image_filename)
						index += 1
						MOTION = False
						
					if DEBUG:
						print("Motion detected on PIR motion sensor.")
		
		# Read output from DHT11 Temperature & Humidity Sensor Module
	
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		if humidity is not None and temperature is not None:
		
			# Alerts MQTT client when an abnormally high temperature is detected (e.g. fire in the kitchen)
			if temperature > 40.0:
							if HIGHTEMP == False:
								HIGHTEMP = True
								image_filename = takeSnapshot(camera)
								image_base64 = convertImageToBase64(image_filename)
								publish_dht11_data(index, humidity, temperature, image_filename, image_base64)
								index += 1
								video_filename = takeVideo(camera)
								uploadFile(video_filename)
								send_mail(image_filename)
								HIGHTEMP = False
				
			if DEBUG:
				print("Humidity={0:0.1f}% Temp={1:0.1f}C".format(humidity, temperature))
			time.sleep(2)
			
		else:
			if DEBUG:
				print("DHT11 sensor failure. Check wiring.")
