import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pathlib import Path

from lib.mzi import heater_with_padding
import gdsfactory as gf
from functools import partial

if __name__ == '__main__':

    WG_CROSS_SECTION = partial(
        gf.cross_section.strip,
        width = 0.5
    )

    component = gf.Component(name='QA_HEATER_PADDING')

    heater_with_padding = heater_with_padding(
        wg_cross_section=WG_CROSS_SECTION,
        heater_length=40.0
    )

    bend_90 = gf.components.bend_euler(
        radius=20, 
        cross_section=WG_CROSS_SECTION
    )

    straight = gf.components.straight(
        length=20, 
        cross_section=WG_CROSS_SECTION
    )

    heater_with_padding_test = component << heater_with_padding

    test_bend_90_left = component  << bend_90
    test_bend_90_left.connect('o2', heater_with_padding_test['o2'])

    test_bend_90_right = component  << bend_90
    test_bend_90_right.mirror_y
    test_bend_90_right.connect('o1', heater_with_padding_test['o1'])

    component.write_gds(
        Path(__file__).parent / 'QA_HEATER_PADDING.gds',
    )
