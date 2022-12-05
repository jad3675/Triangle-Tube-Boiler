#!/usr/bin/env python3
import os, RPi.GPIO as GPIO
from time import sleep
from datadog import initialize, statsd
import logging

# Set up configuration options
options = {
    'statsd_host':'127.0.0.1',
    'statsd_namespace':'Zones',
    'statsd_port':8125
}

# Set up logging
logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

logging.info("starting...")

# Set up GPIO pins and initialize them as inputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)
GPIO.setup(3,GPIO.IN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define a function to check the status of a zone and report it
def check_zone(zone_name, pin):
    # Check the current state of the pin
    if GPIO.input(pin):
        # Pin is high (on)
        logging.info("%s Valve is open!", zone_name)
        statsd.gauge('%s Zone Status' % zone_name, 1, tags=["Zones:%s" % zone_name])
    else:
        # Pin is low (off)
        logging.info("%s Valve is closed!", zone_name)
        statsd.gauge('%s Zone Status' % zone_name, 0, tags=["Zones:%s" % zone_name])

# Register the callback function to be called when the state of a pin changes
GPIO.add_event_detect(2, GPIO.BOTH, callback=check_zone, bouncetime=50, args=["Basement", 2])
GPIO.add_event_detect(3, GPIO.BOTH, callback=check_zone, bouncetime=50, args=["First Floor", 3])
GPIO.add_event_detect(4, GPIO.BOTH, callback=
