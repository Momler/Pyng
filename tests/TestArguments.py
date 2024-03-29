import unittest
from src.Arguments import Arguments


class TestArguments(unittest.TestCase):
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

    def test_a_flag(self):
        arguments = Arguments(["testprogram", "foo.com", "-a"])

        self.assertEqual(arguments.host, "foo.com")
        self.assertEqual(arguments.a_flag, True)

    def test_f_flag(self):
        arguments = Arguments(["testprogram", "foo.com", "-f"])

        self.assertEqual(arguments.host, "foo.com")
        self.assertEqual(arguments.f_flag, True)

    def test_n_flag_no_number(self):
        with self.assertRaises(SystemExit) as cm:
            Arguments(["testprogram", "foo.com", "-n"])

        self.assertEqual(cm.exception.code, -1)

    def test_n_flag(self):
        arguments = Arguments(["testprogram", "foo.com", "-n", "3"])

        self.assertEqual(arguments.host, "foo.com")
        self.assertEqual(arguments.n_flag[0], True)
        self.assertEqual(arguments.n_flag[1], 3)

    def test_l_flag_negative(self):
        with self.assertRaises(SystemExit) as cm:
            Arguments(["testprogram", "foo.com", "-l", "-5"])

        self.assertEqual(cm.exception.code, -1)

    def test_l_flag_too_big(self):
        with self.assertRaises(SystemExit) as cm:
            Arguments(["testprogram", "foo.com", "-l", "99999999"])

        self.assertEqual(cm.exception.code, -1)

    def test_l_flag(self):
        arguments = Arguments(["testprogram", "foo.com", "-l", "12345"])

        self.assertEqual(arguments.host, "foo.com")
        self.assertEqual(arguments.l_flag[0], True)
        self.assertEqual(arguments.l_flag[1], 12345)

    def test_flag_no_host(self):
        with self.assertRaises(SystemExit) as cm:
            Arguments(["testprogram", "-t"])

        self.assertEqual(cm.exception.code, -1)


if __name__ == "__main__":
    unittest.main()
