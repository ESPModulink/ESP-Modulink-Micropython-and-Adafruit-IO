from machine import Pin, Timer, deepsleep
import network
import time
from umqtt.robust import MQTTClient
import sys
import dht
import machine
from time import sleep

sensor = dht.DHT11(Pin(15))                  # DHT11 Sensor on IO15 of ESP32
led=Pin(2,Pin.OUT)
# WIFI_SSID     = 'MERCUSYS_8CA4'
# WIFI_PASSWORD = 'F6bMHDAadT#'

WIFI_SSID     = 'BUAP_Estudiantes'
WIFI_PASSWORD = 'f85ac21de4'

mqtt_client_id      = bytes('client_'+'1', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = 'IsmaMinor'
ADAFRUIT_IO_KEY     = '15c4491a6c9944ebb4d2fcb1f8ae356a'

TEMP_FEED_ID      = 'temp'
HUM_FEED_ID      = 'hum'


wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.disconnect()
wifi.connect(WIFI_SSID,WIFI_PASSWORD)
if not wifi.isconnected():
    print('connecting..')
    timeout = 0
    while (not wifi.isconnected() and timeout < 10):
        print(10 - timeout)
        timeout = timeout + 1
        sleep(1) 
if(wifi.isconnected()):
    print('connected')
else:
    print('not connected')
    led.value(1)
    sleep(2)
    led.value(0)
    sleep(0.5)
    #deepsleep(5000)     #10000ms sleep time   
    deepsleep(60000) 
#connect_wifi() # Connecting to WiFi Router 


client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
#     sys.exit()

        
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8') # format - IsmaMinor/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8') # format - IsmaMinor/feeds/hum   



sensor.measure()                    # Measuring 
temp = sensor.temperature()         # getting Temp
hum = sensor.humidity()
client.publish(temp_feed,    
              bytes(str(temp), 'utf-8'),   # Publishing Temp feed to adafruit.io
              qos=0)

client.publish(hum_feed,    
              bytes(str(hum), 'utf-8'),   # Publishing Hum feed to adafruit.io
              qos=0)
print("Temp - ", str(temp))
print("Hum - " , str(hum))
print('Msg sent')


#sens_data()
# timer = Timer(0)
# timer.init(period=5000, mode=Timer.PERIODIC, callback = sens_data)
sleep(5)

print('Im awake, but Im going to sleep')

#deepsleep(10000)     #10000ms sleep time
deepsleep(900000)   
