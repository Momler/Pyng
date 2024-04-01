class Arguments:
    host = ""
    t_flag = False
    a_flag = False
    n_flag = (False, 0)
    l_flag = (False, 0)

    optional_options = [
        [
            "-t",
            [
                "             Pingt den angegebenen Host bis zur Beendigung des Vorgangs",
                "                    Drücken Sie STRG+UNTBR, um die Statistik anzuzeigen und",
                "                    den Vorgang fortzusetzen.",
                "                    Drücken Sie STRG+C, um den Vorgang abzubrechen.",
            ],
        ],
        ["-a", ["             Löst Adressen zu Hostnamen auf."]],
        ["-n count", ["       Die Anzahl der zu sendenden Echoanforderungen."]],
        ["-l size", ["        Die Größe des Sendepuffers."]],
        ["Zielname", []],
    ]

    def __init__(self, arguments):
        if len(arguments) > 1:
            self.parse(arguments)
        else:
            print(self.create_help_text())
            exit(-1)

    def parse(self, arguments):
        if "-t" in arguments:
            self.t_flag = True
            arguments.remove("-t")

        if "-a" in arguments:
            self.a_flag = True
            arguments.remove("-a")

        if "-n" in arguments:
            n = self.get_flag_value(arguments, "-n")
            self.n_flag = (True, int(n))
            del arguments[arguments.index("-n") + 1]
            arguments.remove("-n")

        if "-l" in arguments:
            l = self.get_flag_value(arguments, "-l")
            self.l_flag = (True, int(l))
            del arguments[arguments.index("-l") + 1]
            arguments.remove("-l")
            if self.l_flag[1] < 0 or self.l_flag[1] > 65500:
                print(
                    "Ungültiger Wert für die Option -l. Der Gültige Bereich liegt zwischen 0 und 65500."
                )
                print("")
                exit(-1)

        if len(arguments) == 1:
            print("IP-Adresse muss angegeben werden.")
            exit(-1)

        self.host = arguments[1]

    def get_flag_value(self, arguments, flag):
        value_index = arguments.index(flag) + 1
        if value_index > len(arguments) - 1:
            print(f"Der Wert muss für die Option angegeben werden {flag}.")
            print("")
            exit(-1)
        else:
            return arguments[value_index]

    def create_help_text(self):
        T = "    "

        flags = ""
        options = ""

        for optional_option in self.optional_options:
            if optional_option[1] == []:
                continue
            flags += f"[{optional_option[0]}] "
            full_option_help = ""

            is_first = True

            for option_help in optional_option[1]:
                if is_first:
                    full_option_help += f" {option_help}\n"
                else:
                    full_option_help += f"{option_help}\n"
                is_first = False
            options += f"{T}{optional_option[0]}{full_option_help}"

        help_text = f"Syntax: ping {flags}\n\nOptionen:\n{options}"
        return help_text
