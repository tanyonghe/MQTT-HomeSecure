import base64
import datetime
from picamera import PiCamera
from time import sleep


def convertImageToBase64(image_filename):
    with open(image_filename, 'b') as image_file:
    encoded = base64.b64encode(image_file.read())
    return encoded

def take_snapshot():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    image_filename = './images/%s.jpg' % (datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'),)
    camera.capture(image_filename)
    camera.stop_preview()
    return image_filename  


if __name__ == '__main__':
    image_filename = take_snapshot()
    print('Took a snapshot photo', image_filename)