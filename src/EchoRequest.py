from WindowsConstants import *

import socket
import struct
import random


class EchoRequest:
    TYPE = 8
    CODE = 0

    def __init__(self):
        self.checksum = 0
        self.id = random.randint(0, 65535)
        self.seq = 1

        self.header = struct.pack(
            "!BBHHH", self.TYPE, self.CODE, self.checksum, self.id, self.seq
        )

        self.checksum = self.calculate_checksum(self.header + PING_PAYLOAD)

        self.packet = (
            struct.pack(
                "!BBHHH",
                self.TYPE,
                self.CODE,
                socket.htons(self.checksum),
                self.id,
                self.seq,
            )
            + PING_PAYLOAD
        )

    def calculate_checksum(self, data):
        checksum = 0
        count_to = (len(data) // 2) * 2

        for count in range(0, count_to, 2):
            this_val = data[count + 1] * 256 + data[count]
            checksum += this_val
            checksum &= 0xFFFFFFFF

        if count_to < len(data):
            checksum += data[-1]
            checksum &= 0xFFFFFFFF

        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum += checksum >> 16
        checksum = ~checksum & 0xFFFF

        return checksum
