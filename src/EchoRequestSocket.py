from PingResult import PingResult
from WindowsConstants import *

import re
import socket
import time


class EchoRequestSocket:

    ping_result = PingResult()

    def __init__(self, packet, arguments):
        self.packet = packet
        self.arguments = arguments
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.sock.settimeout(PING_TIMOUT)

        if arguments.a_flag:
            self.resolve_host_name()

        self.ping_result.host_ip = arguments.host

    def send(self):
        try:
            self.ping_result.sends = self.ping_result.sends + 1
            self.send_time = int(time.time() * 1000)
            self.sock.sendto(self.packet, (self.arguments.host, 0))
            return True
        except Exception as e:
            return False

    def read(self):
        try:
            data, addr = self.sock.recvfrom(1024)

            recv_time = int(time.time() * 1000)

            took_time = recv_time - self.send_time

            self.ping_result.times.append(took_time)
            self.ping_result.successes = self.ping_result.successes + 1

            if self.ping_result.host_name == "":
                print(f"Antwort von {self.ping_result.host_ip}: Zeit={took_time}ms")
            else:
                print(f"Antwort von {self.ping_result.host_name}: Zeit={took_time}ms")
            return True
        except Exception as e:
            print("Zeitüberschreitung der Anforderung")
            return False

    def ping(self):
        print("")
        if self.arguments.l_flag[0]:
            payload_size = self.arguments.l_flag[1]
        else:
            payload_size = DEFAULT_PING_PAYLOAD_SIZE

        if self.ping_result.host_name == "":
            print(
                f"Ping wird ausgeführt für {self.ping_result.host_ip} mit {payload_size} Bytes Daten:"
            )
        else:
            print(
                f"Ping wird ausgeführt für {self.ping_result.host_ip} [{self.ping_result.host_name}] mit {payload_size} Bytes Daten:"
            )

        if self.arguments.t_flag:
            while True:
                send_result = self.send()
                read_result = self.read()
                if not send_result or not read_result:
                    self.ping_result.fails = self.ping_result.fails + 1
                time.sleep(PING_SLEEP)
        else:
            repetitions = PING_REPETITIONS
            if self.arguments.n_flag[0]:
                repetitions = self.arguments.n_flag[1]

            for i in range(repetitions):
                send_result = self.send()
                read_result = self.read()
                if not send_result or not read_result:
                    self.ping_result.fails = self.ping_result.fails + 1
                if i < repetitions - 1:
                    time.sleep(PING_SLEEP)

        lost_percentage = 100
        if self.ping_result.sends > 0:
            lost_percentage = (self.ping_result.fails / self.ping_result.sends) * 100

        lost_percentage = int(lost_percentage)
        self.ping_result.lost_percentage = lost_percentage

        print("")

    def resolve_host_name(self):
        try:
            addr_info = socket.getaddrinfo(self.arguments.host, None, socket.AF_INET6)
            ipv6_addresses = [
                info[4][0] for info in addr_info if info[0] == socket.AF_INET6
            ]
            self.ping_result.host_name = ipv6_addresses[0]
        except:
            print(
                f"""Ping-Anforderung konnte Host "{self.arguments.host}" nicht finden. Überprüfen Sie den Namen, und versuchen Sie es erneut."""
            )
            print("")
            exit(-1)

    def close(self):
        self.sock.close()
