import sys


class Arguments:
    host = ""
    t_flag = False

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

    def __init__(self):
        arguments = sys.argv

        if len(arguments) > 1:
            self.parse(arguments)
        else:
            self.print_help()

    def parse(self, arguments):
        if "-t" in arguments:
            self.t_flag = True
            arguments.remove("-t")

        self.host = arguments[1]

    def print_help(self):
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
        print(help_text)
