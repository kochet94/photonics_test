import unittest

from tests.test_mzi_optical_ports_sanity import TestMziPortsSanity


if __name__ == '__main__':

    failures = 0

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMziPortsSanity)
    runner = unittest.TextTestRunner(verbosity=2)

    print('\n')
    print('MZI PORTS SANITY SECTION')
    print(70 * '-')

    failures += len(runner.run(suite).failures)
