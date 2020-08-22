#!/usr/bin/env python3

import sys
import time

from w1 import Manager, Family

from prometheus_client import CollectorRegistry, Gauge, start_http_server
from prometheus_client.exposition import basic_auth_handler

# temp manager
manager = Manager()


def get_temps():
    temps = {}
    for slave in manager.slaves(family=Family.THERM):
        degrees = slave.celsius
        if 10 < degrees < 40:
            temps[slave.name] = degrees
        print("Temp {}: {}".format(slave.name, degrees))
    return temps


def register_temps():
    registry = CollectorRegistry()
    found = False
    gauges = {}
    while True:
        for name, temp in get_temps().items():
            name = name.replace('28-', '')
            if name not in gauges:
                gauges[name] = Gauge('temperature_{}'.format(name), 'Degrees Celsius')
            gauges[name].set(temp)
            found = True
        if not found:
            print("No sensors found")
            sys.exit(1)
    time.sleep(10)


def run():
    start_http_server(9101)
    register_temps()


if __name__ == "__main__":
    run()
