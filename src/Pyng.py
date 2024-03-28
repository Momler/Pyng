from EchoRequestSocket import EchoRequestSocket
from EchoRequest import EchoRequest
from Arguments import Arguments
from PingStatistics import PingStatistics

import sys

if __name__ == "__main__":
    arguments = Arguments(sys.argv)
    echo_request = EchoRequest()
    request_socket = EchoRequestSocket(echo_request.packet, arguments)

    try:
        request_socket.ping()
    except KeyboardInterrupt:
        # A windows ping doesnt terminate on KeyboardInterrupt, it simply prints the statistics
        print("")

    request_socket.close()

    statistics = PingStatistics(request_socket.ping_result)
    statistics.dump()
