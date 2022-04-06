#!/usr/bin/env python3

import csv
import os
import time
from datadog import initialize, statsd
import logging
from time import sleep


#define datadog
options = {
    'statsd_host':'127.0.0.1',
    'statsd_namespace':'Zones',
    'statsd_port':8125
}


read_interval = 30

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')


sensors = ["28-000000027a48", "28-5638841e64ff", "28-00000002ad87", "28-00000002bd65", "28-00000002d61b", "28-000000030889", "28-c631841e64ff"]
sensors_map = { sensors[0]: "hot_water_temp   = ",
                sensors[1]: "turbo_max_temp = ",
                sensors[2]: "turbo_max_zone_temp = ",
                sensors[3]: "second_zone_temp = ",
                sensors[4]: "basement_zone_temp = ",
                sensors[5]: "main_zone_temp = ",
                sensors[6]: "pipe_return_temp = "}

def c_to_f(temperature_c):
    return 9.0/5.0 * temperature_c + 32


def read_temp(id):
  sensor = "/sys/devices/w1_bus_master1/" + id + "/w1_slave"
  temp = -125.0 # error value
  try:
    f = open(sensor, "r")
    data = f.read()
    f.close()
    if "YES" in data:
      partitioned = data.partition(' t=')
      temp = float(partitioned[2]) / 1000.0
  except Exception:
    pass

  return temp

temps = {}
timenow = time.asctime
while True:
    sleep(read_interval)
    for sensor in sensors:
      temp = read_temp(sensor)
      tempf = c_to_f(temp)
      #print('%s%.2fF' % (sensors_map[sensor], tempf))
      logging.info('%s%.2fF' % (sensors_map[sensor], tempf))
      statsd.gauge(sensors_map[sensor], tempf, tags=["TriangleTube:Boiler"])
      temps[sensor]=tempf
