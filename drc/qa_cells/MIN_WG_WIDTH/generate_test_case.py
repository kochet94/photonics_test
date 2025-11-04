import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pathlib import Path

import gdsfactory as gf
from functools import partial

if __name__ == '__main__':

    WG_CROSS_SECTION_VALID = partial(
        gf.cross_section.strip,
        width = 0.45
    )

    WG_CROSS_SECTION_INVALID_LESS = partial(
        gf.cross_section.strip,
        width = 0.4
    )

    WG_CROSS_SECTION_INVALID_MORE = partial(
        gf.cross_section.strip,
        width = 0.5
    )

    component = gf.Component(name='QA_WAVEGUIDE')

    straight_valid_template = gf.components.straight(
        length=20, 
        cross_section=WG_CROSS_SECTION_VALID
    )

    straight_valid = component << straight_valid_template
    straight_valid.move((0,0))

    straight_invalid_less_template = gf.components.straight(
        length=20, 
        cross_section=WG_CROSS_SECTION_INVALID_LESS
    )

    straight_invalid_less = component << straight_invalid_less_template
    straight_invalid_less.movey(-10)

    straight_invalid_more_template = gf.components.straight(
        length=20, 
        cross_section=WG_CROSS_SECTION_INVALID_MORE
    )

    straight_invalid_more = component << straight_invalid_more_template
    straight_invalid_more.movey(-20)

    component.write_gds(
        Path(__file__).parent / 'QA_WG_WIDTH.gds',
    )
