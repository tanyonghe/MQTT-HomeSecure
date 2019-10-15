import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import time


MQTT_SERVER = "localhost"
MQTT_PATH = "cs3103_group2_channel"


def publish_pir_data():
	publish.single(MQTT_PATH, "Motion detected on PIR motion sensor!", hostname=MQTT_SERVER)


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