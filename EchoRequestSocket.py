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

        try:
            addr_info = socket.getaddrinfo(arguments.host, None, socket.AF_INET6)
            ipv6_addresses = [
                info[4][0] for info in addr_info if info[0] == socket.AF_INET6
            ]
            self.ping_result.host_name = ipv6_addresses[0]
        except:
            if not self.is_valid_ipv4(arguments.host):
                print(
                    f"""Ping-Anforderung konnte Host "{arguments.host}" nicht finden. Überprüfen Sie den Namen, und versuchen Sie es erneut."""
                )
                print("")
                exit(0)
            pass
        self.ping_result.host_ip = arguments.host

    def send(self):
        try:
            self.ping_result.sends = self.ping_result.sends + 1
            self.send_time = int(time.time() * 1000)
            self.sock.sendto(self.packet, (self.arguments.host, 0))
        except Exception as e:
            self.ping_result.fails = self.ping_result.fails + 1

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
        except Exception as e:
            print("Zeitüberschreitung der Anforderung")
            self.ping_result.fails = self.ping_result.fails + 1

    def ping(self, repetitions=4):
        print("")
        if self.ping_result.host_name == "":
            print(
                f"Ping wird ausgeführt für {self.ping_result.host_ip} mit {len(self.packet)} Bytes Daten:"
            )
        else:
            print(
                f"Ping wird ausgeführt für {self.ping_result.host_ip} [{self.ping_result.host_name}] mit {len(self.packet)} Bytes Daten:"
            )

        if self.arguments.t_flag:
            while True:
                self.send()
                self.read()
                time.sleep(PING_SLEEP)
        else:
            for i in range(repetitions):
                self.send()
                self.read()
                if i < repetitions - 1:
                    time.sleep(PING_SLEEP)

        lost_percentage = (self.ping_result.fails / self.ping_result.sends) * 100
        if lost_percentage.is_integer():
            lost_percentage = int(lost_percentage)
        self.ping_result.lost_percentage = lost_percentage

        print("")

    def is_valid_ipv4(self, ip):
        ipv4_pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if re.match(ipv4_pattern, ip):
            return True
        else:
            return False

    def close(self):
        self.sock.close()
