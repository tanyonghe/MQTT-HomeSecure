import base64
import datetime
import math
from picamera import PiCamera
from time import sleep


def convertImageToBase64(image_filename):
	try:
		with open(image_filename, 'b') as image_file:
			encoded = base64.b64encode(image_file.read())
		return encoded
	except:
		print("Failed to encode snapshot photo")

def takeSnapshot():
	try:
		camera = PiCamera()
		camera.start_preview()
		sleep(5)
		image_filename = './images/%s.jpg' % (datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'),)
		camera.capture(image_filename)
		camera.stop_preview()
		return image_filename
	except:
		print("Failed to take snapshot photo")

def takeSnapshotBase64():
	image_filename = takeSnapshot()
	encoded = convertImageToBase64(image_filename)
	return encoded

if __name__ == '__main__':
    image_filename = takeSnapshot()
    print('Took a snapshot photo', image_filename)