import base64
import datetime
import math
from picamera import PiCamera
import time


def convertImageToBase64(image_filename):
	try:
		with open(image_filename, 'b') as image_file:
			encoded = base64.b64encode(image_file.read()).decode("utf-8")
		return encoded
	except:
		print("Failed to encode snapshot photo.")

def takeSnapshot():
	try:
		camera = PiCamera()
		camera.start_preview()
		time.sleep(5)
		image_filename = './images/%s.jpg' % (datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'),)
		camera.capture(image_filename)
		camera.stop_preview()
		return image_filename
	except:
		print("Failed to take snapshot photo.")

if __name__ == '__main__':
    image_filename = takeSnapshot()
    print('Took a snapshot photo', image_filename)