
# Home Surveillance via Data Sensors using MQTT Protocol

To set up a home surveillance system using motion sensors that can send data messages to homeowners.

## Setup
### DHT11 Temperature & Humidity Sensor
GCC - GPIO Pin 2
Data - GPIO Pin 7
GND - GPIO Pin 9
### HC-SR501 PIR Sensor
GCC - GPIO Pin 1
Data - GPIO Pin 11
GND - GPIO Pin 6


## Timeline
Week 10 - Work on delegated tasks
Week 11 - Prep for lab demo
Week 12 - Implement everything else together
Week 13 - Prep for final lab demo

## Work in Progress
1. Design a nice UI for displaying data from our sensors + store messages in json
2. TLS connection using certificates (security)
3. Raspberry Pi Sensor
4. Persistent connection by queueing unsent data messages (in case of service disruptions)
5. Fluff

## Fluff
1.  Well defined primary purpose of IoT project (10%)
2. Ideas for possible future extensions (20%)
3. Specific Algorithms/Methods/Techniques used (30%)
- Where and how the data is processed
- Communication protocols used (e.g. structure of data packet, how often it is sent, duty cycle)
