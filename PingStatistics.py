class PingStatistics:

    def __init__(self, ping_result):
        self.ping_result = ping_result

    def dump(self):
        if self.ping_result.host_name == "":
            print(f"Ping-Statistik für {self.ping_result.host_ip}:")
        else:
            print(f"Ping-Statistik für {self.ping_result.host_name}:")

        print(
            f"    Pakete: Gesendet = {self.ping_result.sends}, Empfangen = {self.ping_result.successes}, Verloren = {self.ping_result.fails}"
        )

        print(f"    ({self.ping_result.lost_percentage}% Verlust), ")

        if self.ping_result.successes > 0:
            sum_times = sum(self.ping_result.times)
            len_times = len(self.ping_result.times)
            mean = sum_times / len_times

            print("Ca. Zeitangaben in Millisek.:")
            print(
                f"    Minimum = {min(self.ping_result.times)}ms, Maximum = {max(self.ping_result.times)}ms, Mittelwert = {mean}ms"
            )
        print("")
