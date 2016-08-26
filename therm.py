#!/usr/bin/python3

# Read temperatures from Raspberry Pi and send to MQTT endpoint.

import click
import json
import ssl
import paho.mqtt.publish as publish
from w1thermsensor import W1ThermSensor
from config import config

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
        temperature=sensor.get_temperature(units)
    ) for sensor in W1ThermSensor.get_available_sensors()]


def publish_temps_aws(temps, config):
    '''Publish temperature readings to AWS IoT.

    temps: iterable
    config: AWS IoT configuration
    '''
    # for each temperature reading, publish to `topic/sensor_id`
    messages = []
    topic = config['topic']
    for t in temps:
        messages.append({
            'topic': '{}/{}'.format(topic, t['sensor_id']),
            'payload': json.dumps(t)
        })

    if messages:
        # configure TLS for secure connection
        certs = config['certs']
        tls = dict(
            ca_certs=certs['ca_certs'],
            certfile=certs['certfile'],
            keyfile=certs['keyfile'],
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None
        )
        publish.multiple(
            messages,
            hostname=config['host'],
            port=config['port'],
            tls=tls
        )

def publish_temps_watson(temps, config):
    '''Publish temperature readings to Watson IoT.

    temps: iterable
    config: Watson IoT configuration
    '''
    for t in temps:
        result = publish.single(
            topic=config['topic'],
            payload=json.dumps(t),
            hostname=config['host'],
            port=config['port'],
            client_id=config['client_id'],
            auth=config['auth']
        )

@click.command()
@click.option('--publish', '-p',
              type=click.Choice(['aws', 'watson']),
              multiple=True)
def cli(publish):
    # read temps from sensors
    temps = read_temperatures()
    print(temps)

    # publish to MQTT endpoints
    for endpoint in publish:
        c = config[endpoint]
        f = globals()['publish_temps_{}'.format(endpoint)]
        f(temps, c)

if __name__ == '__main__':
    cli()
