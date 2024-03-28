from EchoRequestSocket import EchoRequestSocket
from EchoRequest import EchoRequest
from Arguments import Arguments
from PingStatistics import PingStatistics

import socket

if __name__ == "__main__":
    arguments = Arguments()
    echo_request = EchoRequest()
    request_socket = EchoRequestSocket(echo_request.packet, arguments)

    # addr_info = socket.getaddrinfo(arguments.host, None, socket.AF_INET6)

    # ipv6_addresses = [info[4][0] for info in addr_info if info[0] == socket.AF_INET6]

    try:
        request_socket.ping()
    except KeyboardInterrupt:
        print("")  # Just like Windows Ping

    statistics = PingStatistics(request_socket.ping_result)
    statistics.dump()

    request_socket.close()
