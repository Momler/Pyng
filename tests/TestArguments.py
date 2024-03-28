import unittest
from src.Arguments import Arguments


class TestArguments(unittest.TestCase):
    def test_help_text(self):
        arguments = Arguments(["testprogram", "127.0.0.1"])

        actual = arguments.create_help_text()

        expected = "Syntax: ping [-t] [-a] \n\n"
        expected += "Optionen:\n"
        expected += "    -t             Pingt den angegebenen Host bis zur Beendigung des Vorgangs\n"
        expected += "                   Drücken Sie STRG+UNTBR, um die Statistik anzuzeigen und\n"
        expected += "                   den Vorgang fortzusetzen.\n"
        expected += (
            "                   Drücken Sie STRG+C, um den Vorgang abzubrechen.\n"
        )
        expected += "    -a             Löst Adressen zu Hostnamen auf.\n"

        self.assertEqual(actual, expected)

    def test_no_arguments(self):
        # One argument is always passed, the program name
        with self.assertRaises(SystemExit) as cm:
            Arguments(["testprogram"])

        self.assertEqual(cm.exception.code, -1)

    def test_ip_argument(self):
        arguments = Arguments(["testprogram", "127.0.0.1"])

        self.assertEqual(arguments.host, "127.0.0.1")
        self.assertEqual(arguments.t_flag, False)

    def test_name_argument(self):
        arguments = Arguments(["testprogram", "foo.com"])

        self.assertEqual(arguments.host, "foo.com")
        self.assertEqual(arguments.t_flag, False)

    def test_t_flag(self):
        arguments = Arguments(["testprogram", "foo.com", "-t"])

        self.assertEqual(arguments.host, "foo.com")
        self.assertEqual(arguments.t_flag, True)

    def test_t_flag_no_host(self):
        with self.assertRaises(SystemExit) as cm:
            Arguments(["testprogram", "-t"])

        self.assertEqual(cm.exception.code, -1)


if __name__ == "__main__":
    unittest.main()
