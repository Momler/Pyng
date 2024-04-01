from EchoRequestSocket import EchoRequestSocket
from Arguments import Arguments
from PingStatistics import PingStatistics

import sys

if __name__ == "__main__":
    arguments = Arguments(sys.argv)
    request_socket = EchoRequestSocket(arguments)

    try:
        request_socket.ping()
    except KeyboardInterrupt:
        # A windows ping doesnt terminate on KeyboardInterrupt, it simply prints the statistics
        print("")

    statistics = PingStatistics(request_socket.ping_result)
    statistics.dump()
