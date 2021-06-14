#!/usr/bin/env python3

# Get values from Inkbird IBS-TH1 and submit to Datadog via dogstatsD

from time import sleep
from bluepy import btle
from datadog import initialize, statsd
import logging
import sys

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

mac = "10:08:2c:1f:35:94"
read_interval = 30

#define datadog
options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}


def float_value(nums):
    # check if temp is negative
    num = (nums[1]<<8)|nums[0]
    if nums[1] == 0xff:
        num = -( (num ^ 0xffff ) + 1)
    return float(num) / 100

def c_to_f(temperature_c):
    return 9.0/5.0 * temperature_c + 32

def get_readings():
    try:
        dev = btle.Peripheral(mac, addrType=btle.ADDR_TYPE_PUBLIC)
        readings = dev.readCharacteristic(0x28)
        return readings
    except Exception as e:
        logging.error("Error reading BTLE: {}".format(e))
        return False

while True:
    sleep(read_interval)
    readings = get_readings()
    if not readings:
        continue

    logging.debug("raw data: {}".format(readings))

    # little endian, first two bytes are temp_c, second two bytes are humidity
    temperature_c = float_value(readings[0:2])
    humidity = float_value(readings[2:4])
    temperature_f = c_to_f(temperature_c)
   
    logging.info("Turbmax Data: temperature: [{:0.2f}]".format(temperature_f))
    statsd.gauge('turbomax_temp_p', temperature_f, tags=["TriangleTube:TurboMax"])
    
