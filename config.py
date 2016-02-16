
import os

certs = {
    'ca_certs': os.getenv('CA_CERTS_FILE', '/home/pi/.ssh/root-CA.crt'),
    'certfile': os.getenv('CERT_FILE', '/home/pi/.ssh/certificate.pem.crt'),
    'keyfile': os.getenv('KEY_FILE', '/home/pi/.ssh/private.pem.key')
}

mqtt = {
    'host': os.getenv('MQTT_HOST', 'AXCMDMGZ7U2F.iot.us-east-1.amazonaws.com'),
    'port': os.getenv('MQTT_PORT', 8883),
    'topic': os.getenv('MQTT_TOPIC', 'iot/temp')
}
