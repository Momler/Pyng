from PingResult import PingResult
from EchoRequest import EchoRequest
from WindowsConstants import *

import struct
import socket
import time


class EchoRequestSocket:

    ping_result = PingResult()

    def __init__(self, arguments):
        self.arguments = arguments

        if arguments.a_flag:
            self.resolve_host_name()

        self.ping_result.host_ip = arguments.host

    def send(self, sends):
        try:
            echo_request = EchoRequest(self.arguments, sends)
            self.ping_result.sends = sends
            self.send_time = int(time.time() * 1000)
            self.sock.sendto(echo_request.packet, (self.arguments.host, 0))
            return True
        except Exception as e:
            return False

    def read(self):
        try:
            for i in range(5):
                data, addr = self.sock.recvfrom(1024)
                if self.validate_echo_response(data, addr):
                    break
                else:
                    print(
                        "Got an echo reponse which is not for this process, try again"
                    )

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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.sock.settimeout(PING_TIMOUT)

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

        sends = 0

        if self.arguments.t_flag:
            while True:
                sends = sends + 1
                send_result = self.send(sends)
                read_result = self.read()
                if not send_result or not read_result:
                    self.ping_result.fails = self.ping_result.fails + 1
                time.sleep(PING_SLEEP)
        else:
            repetitions = PING_REPETITIONS
            if self.arguments.n_flag[0]:
                repetitions = self.arguments.n_flag[1]

            for i in range(repetitions):
                sends = sends + 1
                send_result = self.send(sends)
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

        self.sock.close()

    def validate_echo_response(self, data, addr):
        # Extract relevant information from the ICMP packet
        (
            response_type,
            response_code,
            response_checksum,
            response_identifier,
            response_sequence,
        ) = struct.unpack("!BBHHH", data[20:28])

        echo_reply = 0
        code = 0

        if response_type != echo_reply:
            print(f"response_type != echo_reply: {response_type != echo_reply}")
            return False
        if response_code != code:
            print(f"response_code != code: {response_code != code}")
            return False

        # print(f"icmp_type={icmp_type}")
        # print(f"icmp_code={icmp_code}")
        # print(f"icmp_checksum={icmp_checksum}")
        # print(f"icmp_identifier={response_identifier}")
        # print(f"icmp_sequence={response_sequence}")
        return True

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
