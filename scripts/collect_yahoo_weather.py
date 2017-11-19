import urllib2, urllib, json, sys
import datetime
from influxdb import InfluxDBClient

baseurl = "https://query.yahooapis.com/v1/public/yql?"
city_woeid="526363"
yql_query = "select atmosphere,item.condition from weather.forecast where woeid = " + city_woeid
yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"

# Set this variables, influxDB should be localhost on Pi
host = "192.168.40.12"
port = 8086
user = "admin"
password = "nimdanimda"
dbname = "smart_home"
measurement = "yahoo_weather_readings"
city = "wroclaw"
repeat = True

def format_float(number):
    return float("%.2f" % round(float(number), 2))

while repeat:
    try:
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)

        #quering yahoo succeed
        repeat = False
        atmosphere = data['query']['results']['channel']['atmosphere']
        condition = data['query']['results']['channel']['item']['condition']
        humidity = atmosphere['humidity']
        pressure = atmosphere['pressure']
        temp_f = condition['temp']
        temp_c = (int(temp_f) - 32)/1.8

        # Create the InfluxDB object
        client = InfluxDBClient(host, port, user, password, dbname)
        current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_body = [
            {
                "measurement": measurement,
                "tags": {
                    "city": city
                },
                "time": current_time,
                "fields": {
                    "temperature" : format_float(temp_c),
                    "humidity" : format_float(humidity),
                    "pressure" : format_float(pressure)
                }
            }]
        # Write JSON to InfluxDB
        client.write_points(json_body)
        print json_body
    except:
        print "Unexpected error:", sys.exc_info()

