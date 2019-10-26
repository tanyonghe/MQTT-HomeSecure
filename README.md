# Home Surveillance via Data Sensors using MQTT Protocol

To set up a home surveillance system using motion sensors that can send data messages to homeowners.

## Project Timeline
Week 10 - Work on delegated tasks  
Week 11 - Prep for lab demo  
Week 12 - Implement everything else together  
Week 13 - Prep for final lab demo  

## Our Setup

### Hardware Used

1. Raspberry Pi
2. Micro SD Card with Raspberry Pi OS image installed
2. F/F Jumper Wires
3. HC-SR501 Infrared PIR Motion Sensor Module
4. DHT11 Temperature & Humidity Sensor Module

### Software Used
 
1. Python 3.7.0  
2. Python Libraries  
* [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) - GPIO Control on a Raspberry Pi  
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
GCC - GPIO Pin 1  
Data - GPIO Pin 11  
GND - GPIO Pin 6  

## Running the Program

1. Start collecting data and publishing messages on the MQTT Broker (i.e. the Raspberry Pi) using the following command in the mqtt_broker directory:

```
python pir_sensor.py
```

2. Subscribe to MQTT Broker (i.e. the Raspberry Pi) on Client Machine (e.g. desktop, laptop, etc.) using the following command in the mqtt_client directory:

```
python mqtt_subscriber.py
```

3. Data will be saved locally and displayed on the HTML page found in the mqtt_client directory.

## Logic Model

1. If motion sensor detects motion, it publishes a data log to the MQTT broker.
2. If temperature sensor detects an abnormally high temperature, it publishes a data log to the MQTT broker.
3. In the cases of both (1) and (2), a snapshot photo will be taken and sent to the client's webpage for remote access.
4. Client can view webpage for logged data when there is detected motion or abnormal temperature in the house.
5. Client can further verify if logged data were false alarms or not by checking the images captured in (3).


## CS3103 Project

### Work in Progress
1. Design a nice UI for displaying data from our sensors + store messages in json
2. TLS connection using certificates (security)
3. Raspberry Pi Sensor
4. Persistent connection by queueing unsent data messages (in case of service disruptions)
5. Fluff

### Fluff
1.  Well defined primary purpose of IoT project (10%)
2. Ideas for possible future extensions (20%)
3. Specific Algorithms/Methods/Techniques used (30%)
- Where and how the data is processed
- Communication protocols used (e.g. structure of data packet, how often it is sent, duty cycle)

## Authors

* **Tan Yong He** - [tanyonghe](https://github.com/tanyonghe)
* **Lou Shaw Yeong** - [xiaoyeong](https://github.com/xiaoyeong)
* **Ng Jian Wei** - [njw95](https://github.com/njw95)
* **Eshwar S/O Kamalapathy** - [eshwarkp](https://github.com/eshwarkp)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration