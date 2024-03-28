class Arguments:
    host = ""
    t_flag = False
    a_flag = False

    optional_options = [
        [
            "-t",
            [
                "Pingt den angegebenen Host bis zur Beendigung des Vorgangs",
                "Drücken Sie STRG+UNTBR, um die Statistik anzuzeigen und",
                "den Vorgang fortzusetzen.",
                "Drücken Sie STRG+C, um den Vorgang abzubrechen.",
            ],
        ],
        ["-a", ["Löst Adressen zu Hostnamen auf."]],
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

        if len(arguments) == 1:
            print("IP-Adresse muss angegeben werden.")
            exit(-1)

        self.host = arguments[1]

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
                    full_option_help += f" {T}{T}{T}{option_help}\n"
                else:
                    full_option_help += f"{T}{T}{T}{T}   {option_help}\n"
                is_first = False
            options += f"{T}{optional_option[0]}{full_option_help}"

        help_text = f"Syntax: ping {flags}\n\nOptionen:\n{options}"
        return help_text
