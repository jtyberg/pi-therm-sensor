import os

config = {
    "aws": {
        "host": os.getenv("AWS_MQTT_HOST", "ab0k2jox2x4ji.iot.us-east-1.amazonaws.com"),
        "port": os.getenv("AWS_MQTT_PORT", 8883),
        "topic": os.getenv("AWS_MQTT_TOPIC", "iot/temp"),
        "certs": {
            "ca_certs": os.getenv("AWS_CA_CERTS_FILE", "/home/pi/.ssh/root-CA.crt"),
            "certfile": os.getenv("AWS_CERT_FILE", "/home/pi/.ssh/certificate.pem.crt"),
            "keyfile": os.getenv("AWS_KEY_FILE", "/home/pi/.ssh/private.pem.key")
        }
    },

    "watson": {
        "org": "org_id",
        "host": "org_id.messaging.internetofthings.ibmcloud.com",
        "port": 1883,
        "topic": "iot-2/evt/temperature/fmt/json",
        "auth": {
            "username": "use-token-auth",
            "password": "my-device-token"
        },
        "client_id": "d:org_id:device_type:device_id"
    }
}
