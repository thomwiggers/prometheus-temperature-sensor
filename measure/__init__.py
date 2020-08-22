#!/usr/bin/env python3

import time

from w1 import Manager, Family

from prometheus_client import CollectorRegistry, Gauge, start_http_server
from prometheus_client.exposition import basic_auth_handler

# Prometheus info
HOST = 'cocytus:9091'
USERNAME = ''
PASSWORD = ''

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


def register_temps(temps):
    registry = CollectorRegistry()
    found = False
    for name, temp in temps.items():
        name = name.replace('28-', '')
        g = Gauge('temperature_{}'.format(name),
                  'Degrees Celsius', registry=registry)
        g.set(temp)
        found = True
    if not found:
        print("No sensors found")
    try:
        push_to_gateway(
            HOST, job='pushgateway',
            registry=registry, handler=my_auth_handler)
    except:
        pass


def run():
    start_http_server(9101)
    while True:
        register_temps(get_temps())
        time.sleep(30)


if __name__ == "__main__":
    run()
