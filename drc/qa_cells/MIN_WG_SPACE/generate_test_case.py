import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pathlib import Path

import gdsfactory as gf
from functools import partial

if __name__ == '__main__':

    WG_CROSS_SECTION = partial(
        gf.cross_section.strip,
        width = 0.5
    )

    component = gf.Component(name='QA_WAVEGUIDE')

    straight_template = gf.components.straight(
        length=20, 
        cross_section=WG_CROSS_SECTION
    )

    straight_valid = component << straight_template
    straight_valid.move((0,0))

    straight_invalid_top = component << straight_template
    straight_invalid_top.movey(1)

    straight_invalid_bottom = component << straight_template
    straight_invalid_bottom.movey(-1)

    straight_invalid_left = component << straight_template
    straight_invalid_left.movex(-20.5)

    straight_invalid_right = component << straight_template
    straight_invalid_right.movex(20.5)

    component.write_gds(
        Path(__file__).parent / 'QA_MIN_WG_SPACE.gds',
    )
