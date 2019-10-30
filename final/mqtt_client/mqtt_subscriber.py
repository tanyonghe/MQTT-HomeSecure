import base64
import datetime
import json
import os
import paho.mqtt.client as mqtt

 
MQTT_SERVER = "192.168.1.28"		# MQTT Broker IP Address
#MQTT_SERVER = "192.168.43.223"		# MQTT Broker IP Address
MQTT_PATH = "cs3103_group2_channel"	# Channel Name
DATA_FILEPATH = "./localhost/public/data/"
DATA_FILENAME = "data.txt"
DATA_FULLPATH = os.path.join(DATA_FILEPATH, DATA_FILENAME)
DEBUG = True


def write_pir_data(data):
	write_data = "%s|||%s|||%s|||%s|||%s\r\n" % (data["index"], "Motion Detected", data["datetime"], data["location"], data["image_filename"])
	
	image_fullpath = os.path.join(DATA_FILEPATH, data["image_filename"])
	with open(image_fullpath, "wb") as f:
		f.write(base64.b64decode(data["image_base64"].encode("utf-8")))
	
	# Read existing data
	try:
		f = open(DATA_FULLPATH, "r")
		old_data = f.read()
		f.close()
	except:
		old_data = ""
		if DEBUG:
			print("%s not found. Creating new file." % (DATA_FILENAME,))

	# Write in new data and append previous data
	if DEBUG:
		print("Writing to %s now..." % (DATA_FILENAME,))
	f = open(DATA_FULLPATH, "w+")
	f.write(write_data)
	f.write(old_data)
	f.close()
	if DEBUG:
		print("Finished writing data.")

	
def write_dht11_data(data):
	write_data = "%s|||%s|||%s|||%s|||%s\r\n" % (data["index"], "Abnormal Temperature Detected: %s" % (data["temperature"],), 
			data["datetime"], data["location"], data["image_filename"])
			
	image_fullpath = os.path.join(DATA_FILEPATH, data["image_filename"])
	with open(image_fullpath, "wb") as f:
		f.write(base64.b64decode(data["image_base64"].encode("utf-8")))
	
	# Read existing data
	try:
		f = open(DATA_FULLPATH, "r")
		old_data = f.read()
		f.close()
	except:
		old_data = ""
		if DEBUG:
			print("%s not found. Creating new file." % (DATA_FILENAME,))
	
	# Write in new data and append previous data
	if DEBUG:
		print("Writing to %s now..." % (DATA_FILENAME,))
	f = open(DATA_FULLPATH, "w+")
	f.write(write_data)
	f.write(old_data)
	f.close()
	if DEBUG:
		print("Finished writing data.")
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code", str(rc))
 
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(MQTT_PATH)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if DEBUG:
		print("Message received from MQTT broker.")
	
	payload = msg.payload.decode("ascii")
	data = json.loads(payload)
	
	if data["topic"] == "pir":
		write_pir_data(data)
		if DEBUG:
			print("It's a PIR data message.")
	else:
		write_dht11_data(data)
		if DEBUG:
			print("It's a DHT11 data message.")


if __name__ == "__main__": 
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_SERVER, 1883, 60)
	 
	# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a manual interface.
	client.loop_forever()