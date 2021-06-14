#!/usr/bin/env python3
from datadog import initialize, statsd
import time
import minimalmodbus
import logging
from time import sleep

#define datadog
options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

read_interval = 30

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

def get_readings():
    try:
        boiler = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
        boiler.serial.baudrate = 38400
        readings  = boiler.read_registers(768,9,4)
        return readings
    except Exception as e:
        logging.error("Error reading ModBus: {}".format(e))
        return False

def c_to_f(temperature_c):
    return 9.0/5.0 * temperature_c + 32

while True:
    sleep(read_interval)
    readings = get_readings()
    if not readings:
        continue
    print(readings)
    boiler_supply_temp = c_to_f(readings[0]/10)
    boiler_return_temp = c_to_f(readings[1])
    boiler_flue_temp = c_to_f(readings[3])
    boiler_outdoor_temp = (readings[4])
    if boiler_outdoor_temp == 32768:
                boiler_outdoor_temp = 0
    boiler_flame_ion = readings[6]
    boiler_firing_rate = readings[7]
    boiler_set_point = (readings[8])
    if boiler_set_point == 32768:
                boiler_set_point = 0

    logging.info("Boiler data: Supply Temp[{:0.2f}], Return Temp[{:0.2f}], Flue Temp[{:0.2f}], Firing Rate[{:0.2%}], Set Point[{:0.2f}], Outdoor Temp[{:0.2f}]".format(boiler_supply_temp, boiler_return_temp, boiler_flue_temp, boiler_firing_rate, boiler_set_point, boiler_outdoor_temp))
    #Send it to the doghole
    statsd.gauge('boiler_supply_temp_p', boiler_supply_temp, tags=["TriangleTube:Boiler"])
    statsd.gauge('boiler_return_temp_p', boiler_return_temp, tags=["TriangleTube:Boiler"])
    statsd.gauge('boiler_flue_temp_p', boiler_flue_temp, tags=["TriangleTube:Boiler"])
    statsd.gauge('boiler_outdoor_temp_p', boiler_outdoor_temp, tags=["TriangleTube:Boiler"])
    statsd.gauge('boiler_flame_ion_p', boiler_flame_ion, tags=["TriangleTube:Boiler"])
    statsd.gauge('boiler_firing_rate_p', boiler_firing_rate, tags=["TriangleTube:Boiler"])
    statsd.gauge('boiler_set_point_p', boiler_set_point, tags=["TriangleTube:Boiler"])
