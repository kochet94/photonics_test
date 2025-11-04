import unittest

from test_mzi_optical_ports_sanity import TestMziOpticalPortsSanity
from test_qa_cells_drc import TestQaCellsDrc


if __name__ == '__main__':

    failures = 0

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMziOpticalPortsSanity)
    runner = unittest.TextTestRunner(verbosity=2)

    print('\n')
    print('MZI PORTS SANITY SECTION')
    print(70 * '-')

    failures += len(runner.run(suite).failures)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestQaCellsDrc)
    runner = unittest.TextTestRunner(verbosity=2)

    print('\n')
    print('QA CELLS DRC SECTION')
    print(70 * '-')

    failures += len(runner.run(suite).failures)