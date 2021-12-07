#!/usr/bin/env python
import os, RPi.GPIO as GPIO
from time import sleep
from datadog import initialize, statsd
import logging

options = {
    'statsd_host':'127.0.0.1',
    'statsd_namespace':'Zones',
    'statsd_port':8125
}

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

logging.info("starting...")
#Set zone status to zero

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)
GPIO.setup(3,GPIO.IN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
  sleep(15);
  if(GPIO.wait_for_edge(2, GPIO.RISING, timeout=50)):
    logging.info("Basement Valve Open!")
    statsd.gauge('Basement Zone Status', 1, tags=["Zones:Basement"])
    sleep(3);
  else:
    logging.info("Basement valve is closed!")
    statsd.gauge('Basement Zone Status', 0, tags=["Zones:Basement"])

  if(GPIO.wait_for_edge(3, GPIO.RISING, timeout=50)):
    logging.info("1st Floor Valve Open!")
    statsd.gauge('First Floor Zone Status', 1, tags=["Zones:First"])
    sleep(3);
  else:
    logging.info("1st Floor valve is closed!")
    statsd.gauge('First Floor Zone Status', 0, tags=["Zones:First"])

  if(GPIO.wait_for_edge(4, GPIO.RISING, timeout=50)):
    logging.info("2nd Floor Valve is open!")
    statsd.gauge('Second Floor Zone Status', 1, tags=["Zones:Second"])
    sleep(3);
  else:
    logging.info("2nd Floor Valve is closed!")
    statsd.gauge('Second Floor Zone Status', 0, tags=["Zones:Second"])
