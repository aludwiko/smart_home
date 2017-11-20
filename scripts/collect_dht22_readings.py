import time
import sys
import datetime
from influxdb import InfluxDBClient
#import automationhat
import RPi.GPIO as GPIO
import Adafruit_DHT

# Set this variables, influxDB should be localhost on Pi
host = "192.168.40.12"
port = "8086"
user = "admin"
password = "nimdanimda"
dbname = "smart_home"
measurement = "DHT22_readings"
room = "bedroom"

# For GPIO
sensor = Adafruit_DHT.DHT22
pin = 22

# Allow user to set session and runno via args otherwise auto-generate
now = datetime.datetime.now()

# Create the InfluxDB object
client = InfluxDBClient(host, port, user, password, dbname)

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
# Note that sometimes you won't get a reading and the results will be null (because Linux can't guarantee the timing of calls to read the sensor). If this happens try again!
if humidity is not None and temperature is not None:
    #print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body = [
        {
            "measurement": measurement,
            "tags": {
                "room": room
            },
            "time": current_time,
            "fields": {
                "temperature" : float("%.2f" % round(temperature, 2)),
                "humidity" : float("%.2f" % round(humidity, 2))
            }
        }]
    # Write JSON to InfluxDB
    client.write_points(json_body)
    print json_body
else:
    print 'Failed to get reading. Try again!'