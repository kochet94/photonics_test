__unittest = True

import unittest

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lib.mzi import mzi

class TestMziOpticalPortsSanity(unittest.TestCase):

    EXPECTED_PORTS = {
        'o1': {
            'type' : 'optical',
            'orientation' : 180.0
        },
        'o2': {
            'type' : 'optical',
            'orientation' : 180.0
        },
        'o3': {
            'type' : 'optical',
            'orientation' : 0.0
        },
        'o4': {
            'type' : 'optical',
            'orientation' : 0.0
        }
    }

    def test_ports_presence(self):

        mzi_component = mzi()
        ports_filtered = filter(lambda x: x.port_type != 'electrical', mzi_component.ports)

        for port in ports_filtered:
            self.assertIn(port.name, self.EXPECTED_PORTS.keys())
            self.assertEqual(port.port_type, self.EXPECTED_PORTS[port.name]['type'])
            self.assertEqual(port.orientation, self.EXPECTED_PORTS[port.name]['orientation'])
