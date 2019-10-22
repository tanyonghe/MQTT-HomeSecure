# Home Surveillance via Data Sensors using MQTT Protocol

To set up a home surveillance system using motion sensors that can send data messages to homeowners.

## Our Setup

Hardware Used

1. Raspberry Pi
2. Micro SD Card with Raspberry Pi OS image installed
2. F/F Jumper Wires
3. HC-SR501 Infrared PIR Motion Sensor Module
4. DHT11 Temperature & Humidity Sensor Module

Software Used
 
1. Python 3.7.0
2. Python Libraries
* [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) - GPIO Control on a Raspberry Pi
```
pip install RPi.GPIO
```
* [Eclipse Paho MQTT Python Client Library](https://pypi.org/project/paho-mqtt/) - Client Class for MQTT Protocol
```
pip install paho-mqtt
```

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


## Authors

* **Tan Yong He** - [tanyonghe](https://github.com/tanyonghe)
* **Lou Shaw Yeong** - [xiaoyeong](https://github.com/xiaoyeong)
* **Ng Jian Wei** - [PurpleBooth](https://github.com/PurpleBooth)
* **Eshwar S/O Kamalapathy** - [eshwarkp](https://github.com/eshwarkp)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration