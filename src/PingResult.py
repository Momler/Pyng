import socket
import struct
import random
import time


class PingResult:

    times = []
    sends = 0
    successes = 0
    fails = 0
    lost_percentage = 0
    host_name = ""
    host_ip = ""
