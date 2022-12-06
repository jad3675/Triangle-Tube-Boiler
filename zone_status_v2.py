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

# Define a callback function to be called when the state of a pin changes
def handle_pin_change(pin):
    # Check the current state of the pin
    if GPIO.input(pin):
        # Pin is high (on)
        if pin == 2:
            logging.info("Basement Valve Open!")
            statsd.gauge('Basement Zone Status', 1, tags=["Zones:Basement"])
        elif pin == 3:
            logging.info("1st Floor Valve Open!")
            statsd.gauge('First Floor Zone Status', 1, tags=["Zones:First"])
        elif pin == 4:
            logging.info("2nd Floor Valve is open!")
            statsd.gauge('Second Floor Zone Status', 1, tags=["Zones:Second"])
    else:
        # Pin is low (off)
        if pin == 2:
            logging.info("Basement valve is closed!")
            statsd.gauge('Basement Zone Status', 0, tags=["Zones:Basement"])
        elif pin == 3:
            logging.info("1st Floor valve is closed!")
            statsd.gauge('First Floor Zone Status', 0, tags=["Zones:First"])
        elif pin == 4:
            logging.info("2nd Floor Valve is closed!")
            statsd.gauge('Second Floor Zone Status', 0, tags=["Zones:Second"])

# Register the callback function to be called when the state of a pin changes
GPIO.add_event_detect(2, GPIO.BOTH, callback=handle_pin_change)
GPIO.add_event_detect(3, GPIO.BOTH, callback=handle_pin_change)
GPIO.add_event_detect(4, GPIO.BOTH, callback=handle_pin_change)

# Main loop
