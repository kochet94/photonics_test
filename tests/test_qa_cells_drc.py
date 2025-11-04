__unittest = True

import unittest
import subprocess

from pathlib import Path

class TestQaCellsDrc(unittest.TestCase):

    def test_ports_presence(self):

        keep_out_heater_drc = Path()