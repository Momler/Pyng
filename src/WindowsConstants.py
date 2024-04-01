PING_SLEEP = 1  # seconds
PING_TIMOUT = 4  # seconds
PING_REPETITIONS = 4
MAX_PAYLOAD_SIZE = 65500
DEFAULT_PING_PAYLOAD_SIZE = 32


def create_ping_payload(size):
    # Windows implementation doesnt put the whole alphabet into the payload, it restarts at w
    alphabet = "abcdefghijklmnopqrstuvw"
    length = len(alphabet)
    result = ""
    for i in range(size):
        result += alphabet[i % length]
    return result.encode()
