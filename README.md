# Home Surveillance via Data Sensors using MQTT Protocol

To set up a home surveillance system using sensors that can send data messages to alert homeowners of suspicious activities like unexpected motions (e.g. intruders) or abnormal temperatures (e.g. fire) and sends them an image so that they can monitor the situation remotely.

## Our Setup

### Hardware Used

1. Raspberry Pi
2. Micro SD Card with Raspberry Pi OS image installed
2. F/F Jumper Wires
3. HC-SR501 Infrared PIR Motion Sensor Module
4. DHT11 Temperature & Humidity Sensor Module
5. Raspberry Pi Camera Module

### Software Used
 
1. Python 3.7.0  
2. Python Libraries  
* [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) - GPIO Control on a Raspberry Pi  
* [Eclipse Mosquitto](https://mosquitto.org/) - Helps to set up MQTT Broker 
* [Eclipse Paho MQTT Python Client Library](https://pypi.org/project/paho-mqtt/) - Client Class for MQTT Protocol   
* [picamera](https://pypi.org/project/picamera/) - Raspberry Pi Camera Module  

Install prerequisite Python libraries with pip:  
```
pip install -r requirements.txt  
```

### RPi GPIO Setup

#### DHT11 Temperature & Humidity Sensor
GCC - GPIO Pin 2  
Data - GPIO Pin 7  
GND - GPIO Pin 9  
#### HC-SR501 PIR Sensor
GCC - GPIO Pin 4  
Data - GPIO Pin 11  
GND - GPIO Pin 6  

## Running the Program

1. Set up Mosquitto MQTT Broker

```
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
```

2. Start collecting data on the MQTT Broker (i.e. the Raspberry Pi) and publishing messages to your MQTT Client Machine (e.g. desktop, laptop, etc.) by using the following command in the `src/broker` directory:

```
python mqtt_sensors.py
```

3. Subscribe to MQTT Broker (i.e. the Raspberry Pi) on your MQTT Client Machine (e.g. desktop, laptop, etc.) using the following command in the `src/client` directory:

```
python mqtt_subscriber.py
```

4. Data (i.e. data logs and images) will be saved locally in the `src/client/localhost/public/data` directory.

5. Alternatively, users may view the data on a deployed Node.js page found in the `src/client/localhost` directory.  
Use the following command to set up the page on `http://localhost:3000`.

```
npm install
node index
```

## Logic Model

1. If motion sensor detects motion, it publishes a data log to the MQTT broker.
2. If temperature sensor detects an abnormally high temperature, it publishes a data log to the MQTT broker.
3. In the cases of both (1) and (2), a snapshot image will be taken and sent to the client's webpage for remote access.
4. Client can view webpage for logged data when there is detected motion or abnormal temperature in the house.
5. Client can further verify if logged data were false alarms or not by checking the images captured in (3).

## Implemented Features

1. Data collection (logs and images) from sensor modules (RPi Camera, PIR Motion, Temperature and Humidity) -YH
2. Format JSON objects from collected data -YH
3. MQTT protocol from MQTT broker and data sensors to MQTT client -YH
4. Storage of data logs and captured images from data sensors -YH
5. UI for displaying logged data on localhost website -YH
6. Enabled TLS connection -YH
7. Enhanced messaging reliability and persistence with MQTT protocol -not done

## Authors

* **Tan Yong He** - [tanyonghe](https://github.com/tanyonghe)
* **Lou Shaw Yeong** - [xiaoyeong](https://github.com/xiaoyeong)
* **Ng Jian Wei** - [njw95](https://github.com/njw95)
* **Eshwar S/O Kamalapathy** - [eshwarkp](https://github.com/eshwarkp)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
