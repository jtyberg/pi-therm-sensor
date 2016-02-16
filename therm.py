#!/usr/bin/python3

# Read temperatures from Raspberry Pi and send to MQTT endpoint.

import argparse
import json
import ssl
import paho.mqtt.publish as publish
from w1thermsensor import W1ThermSensor

def read_temperatures(units=W1ThermSensor.DEGREES_F):
    '''Read temperatures from attached thermometers.

    Parameters
    units: int default=W1ThermSensor.DEGREES_F
        Temerature units (e.g., Fahrenheit, Celcius, Kelvin) as

    Returns
    array of dicts, each one containing sensor ID and temperature reading
        `[
            {
             'sensor_id': '80000002d2e0',
             'sensor_type': 'DS18B20',
             'temperature': 63.16160000000001
             },
            {
             'sensor_id': '80000002d4c1',
             'sensor_type': 'DS18B20',
             'temperature': 20.8740000000001
             }
         ]`
    '''
    return [dict(
        sensor_id=sensor.id,
        sensor_type=sensor.type_name,
        temperature=sensor.get_temperature(_units)
    ) for sensor in W1ThermSensor.get_available_sensors()]

def publish_temperatures(temps):
    '''Publish temperature readings to MQTT endpoint.

    temps: iterable
    '''
    from config import certs, mqtt

    # configure TLS for secure connection
    tls = dict(
        ca_certs=certs['ca_certs'],
        certfile=certs['certfile'],
        keyfile=certs['keyfile'],
        tls_version=ssl.PROTOCOL_TLSv1_2,
        ciphers=None
    )

    # for each temperature reading, publish to `topic/sensor_id`
    messages = []
    for t in temps:
        messages.append({
            'topic': '{}/{}'.format(mqtt['topic'], t['sensor_id']),
            'payload': json.dumps(t)
        })
    if messages:
        return publish.multiple(
            messages,
            hostname=mqtt['host'],
            port=mqtt['port'],
            tls=tls
        )

def main():
    # parse command line args to see if temps should be published
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true',
                        help='publish temperature readings')
    args = parser.parse_args()

    # read temps from sensors
    temps = read_temperatures()
    print(temps)

    # publish temps to MQTT endpoint
    if args.publish:
        publish_temperatures(temps)

if __name__ == '__main__':
    main()
