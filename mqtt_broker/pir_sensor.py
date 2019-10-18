import Adafruit_DHT
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import time


MQTT_SERVER = "localhost"
MQTT_PATH = "cs3103_group2_channel"
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4


def publish_pir_data():
	publish.single(MQTT_PATH, "PIR Sensor: Motion Detected!", hostname=MQTT_SERVER)

def publish_dht11_data(humidity, temperature):
	publish.single(MQTT_PATH, "DHT11 {0:0.1f}% {1:0.1f}C".format(humidity, temperature), hostname=MQTT_SERVER)

if __name__ == "__main__":
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
	#GPIO.setup(3, GPIO.OUT)		#LED output pin
	while True:
		i = GPIO.input(11)
		if i == 0:					#When output from motion sensor is LOW
			#GPIO.output(3, 0)		#Turn OFF LED
			time.sleep(1)
		elif i == 1:				#When output from motion sensor is HIGH
			print("Motion detected on PIR motion sensor!")
			publish_pir_data()		#Publish data to subscribers
			#GPIO.output(3, 1)  	#Turn ON LED
			time.sleep(1)
			
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		if humidity is not None and temperature is not None:
			publish_dht11_data(humidity, temperature)
			print("Humidity={0:0.1f}% Temp={1:0.1f}C".format(humidity, temperature))
		else:
			print("Sensor failure. Check wiring.")