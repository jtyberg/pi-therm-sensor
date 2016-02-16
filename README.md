# pi-therm-sensor

Sample code for reading temperatures from DS18B20 sensors connected to a Raspberry Pi, and sending them to an MQTT endpoint (in this case, AWS IoT).

## Raspberry Pi hardware setup

See the [AdaFruit tutorial](http://www.reuk.co.uk/DS18B20-Temperature-Sensor-with-Raspberry-Pi.htm) for useful instructions on connecting the DS18B20 sensors to the Pi.

## AWS IoT setup

This sample sends temperature readings to the [AWS IoT](https://aws.amazon.com/iot/) device gateway using the MQTT protocol.  For it to work, the Pi must be a registered thing on AWS IoT, it must be authorized to connect to AWS, and it must be allowed to publish messages to the AWS IoT device gateway.  In short:

* create a thing on AWS IoT as a virtual representation of the Pi
* create a security certificate on AWS IoT, download the cert, private key and public key files, and copy them to the Pi
* attach the Pi thing to the certificate
* create a policy that allows publishing to any topic
* attach the policy to the certificate

This guide on getting started with [AWS IoT and Raspberry Pi](http://blog.getflint.io/get-started-with-aws-iot-and-raspberry-pi) is useful.

## Run the code

1. Copy the AWS certificate files and the [root CA certificate file](https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem) to the Pi.

2. Download this code to the Pi.

  ```
  cd /home/pi

  git clone git@github.com:jtyberg/pi-therm-sensor.git
  ```

3. Modify the certificate and key file paths, and the MQTT endpoints in `config.py`.

4. Install Python package dependencies on the Pi.  This sample uses the [W1ThermSensor](https://github.com/timofurrer/w1thermsensor) package to read from the sensors connected to the Pi, and the [paho-mqtt](https://www.eclipse.org/paho/clients/python/) package to send the data to AWS IoT endpoints.

  ```
  pip3 install w1thermsensor paho-mqtt
  ```

5. Run it

  ```
  cd /home/pi/pi-therm-sensor

  # just print the temperature readings to the console
  python3 therm.py

  # print the temperatures to the console and publish them to MQTT endpoint
  python3 therm.py --publish
  ```

To setup a cron job to read and publish temperatures every 15 minutes:

```
crontab -l | { cat; echo "0,15,30,45 * * * * /home/pi/pi-therm-sensor/therm.py --publish"; } | crontab -
```
