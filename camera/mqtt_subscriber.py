import datetime
import json
import paho.mqtt.client as mqtt

 
MQTT_SERVER = "192.168.43.223"		# MQTT Broker IP Address
MQTT_PATH = "cs3103_group2_channel"	# Channel Name


def write_pir_data():
	write_data = "%s|||%s|||%s|||%s|||%s" % (data["index"], "Motion Detected", data["datetime"], data["location"], data["image_filename"])
	
	# Read existing data
	try:
		f = open("data.txt", "r")
		old_data = f.read()
		f.close()
	except:
		old_data = ""
	
	# Write in new data and append previous data
	f = open("data.txt", "w+")
	f.write(write_data)
	f.write(old_data)
	f.close()
	
def write_dht11_data(data):
	write_data = "%s|||%s|||%s|||%s|||%s" % (data["index"], "Abnormal Temperature Detected: %s" % (data["temperature",), 
			data["datetime"], data["location"], data["image_filename"])
	
	# Read existing data
	try:
		f = open("data.txt", "r")
		old_data = f.read()
		f.close()
	except:
		old_data = ""
	
	# Write in new data and append previous data
	f = open("data.txt", "w+")
	f.write(write_data)
	f.write(old_data)
	f.close()
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code", str(rc))
 
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic, str(msg.payload))
	payload = msg.payload.decode("utf-8")
	data = json.loads(payload)
	if data["topic"] == "pir":
		write_pir_data(data)
	else:
		pass
		write_dht11_data(data)
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_forever()
