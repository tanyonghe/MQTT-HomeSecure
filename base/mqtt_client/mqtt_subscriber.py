import datetime
import paho.mqtt.client as mqtt

 
MQTT_SERVER = "192.168.1.28"
MQTT_PATH = "cs3103_group2_channel"


def write_pir_data():
	# Read existing data
	try:
		f = open("pir_data.txt", "r")
		data = f.read()
		f.close()
	except:
		data = ""
	
	# Write in new data and append previous data
	f = open("pir_data.txt", "w+")
	f.write("Motion detected on %s\r\n" % (datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),))
	f.write(data)
	f.close()
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
 
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	f = open("pir_data.txt", "a+")
	f.write("Motion detected on %s\r\n" % (datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),))
	f.close()
	# more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_forever()
