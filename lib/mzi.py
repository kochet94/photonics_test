import gdsfactory as gf
import gdsfactory.generic_tech as tech
from gdsfactory.technology import LayerMap

from functools import partial


class LayerMap(LayerMap):
    DRC_TEXT = (66, 1)


@gf.cell()
def heater_with_padding(
    wg_cross_section: gf.cross_section,
    heater_length: float = 40.0,
    padding: float = 2.0
) -> gf.component:
    
    component = gf.Component()
    
    HEATER_METAL_CROSS_SECTION = partial(
        gf.cross_section.heater_metal,
        width = 5 * wg_cross_section.keywords['width'],
    )

    HEATER_WG_CROSS_SECTION = partial(
        gf.cross_section.strip_heater_metal, 
        width=wg_cross_section.keywords['width'],
        heater_width= 5 * wg_cross_section.keywords['width']
    )

    heater = gf.components.straight_heater_metal(
        length=heater_length,
        cross_section=wg_cross_section,
        cross_section_waveguide_heater=HEATER_WG_CROSS_SECTION,
        cross_section_heater=HEATER_METAL_CROSS_SECTION,
    )

    component << heater

    #adding padding for heater in order to implement a keep-out zone
    gf.add_padding(component, default=padding)

    #propagate optical/electrical ports
 
    component.add_port("o1", port=heater.ports["o1"])
    component.add_label(
        text="DRC_INTERCONNECTION", 
        position=(
            component.ports["o1"].x,
            component.ports["o1"].y
        ),
        layer=LayerMap.DRC_TEXT
    )
    component.add_port("o2", port=heater.ports["o2"])
    component.add_label(
        text="DRC_INTERCONNECTION", 
        position=(
            component.ports["o2"].x,
            component.ports["o2"].y
        ),
        layer=LayerMap.DRC_TEXT
    )

    component.add_port("l_e1", port=heater.ports["l_e1"])
    component.add_port("l_e2", port=heater.ports["l_e2"])
    component.add_port("l_e3", port=heater.ports["l_e3"])
    component.add_port("l_e4", port=heater.ports["l_e4"])

    component.add_port("r_e1", port=heater.ports["r_e1"])
    component.add_port("r_e2", port=heater.ports["r_e2"])
    component.add_port("r_e3", port=heater.ports["r_e3"])
    component.add_port("r_e4", port=heater.ports["r_e4"])

    return component

@gf.cell()
def mzi(
    delta_l: float = 10.0,
    wg_width: float = 0.5, 
    bend_radius: float = 10.0, 
    heater_length: float = 40.0,
    padding: float = 2.0
) -> gf.component:
    

    WG_CROSS_SECTION = partial(
        gf.cross_section.strip,
        width = wg_width
    )

    component = gf.Component()
    
    #initializing components

    coupler = gf.components.coupler(
        cross_section=WG_CROSS_SECTION
    )

    bend_90 = gf.components.bend_euler(
        radius=bend_radius, 
        cross_section=WG_CROSS_SECTION
    )

    straight_delta_l = gf.components.straight(
        length=delta_l, 
        cross_section=WG_CROSS_SECTION
    )

    straight_heater = heater_with_padding(
        wg_cross_section=WG_CROSS_SECTION,
        padding=padding
    )

    straight_non_heater = gf.components.straight(
        length=heater_length, 
        cross_section=WG_CROSS_SECTION
    )

    #creating and connecting instances

    coupler_left = component << coupler

    bend_top_left_one = component << bend_90
    bend_top_left_one.connect('o1', coupler_left.ports['o3'])

    bend_bottom_left_one = component << bend_90
    bend_bottom_left_one.mirror_y()
    bend_bottom_left_one.connect('o1', coupler_left.ports['o4'])

    straight_delta_l_left = component << straight_delta_l
    straight_delta_l_left.connect('o1', bend_top_left_one.ports['o2'])

    bend_top_left_two = component << bend_90
    bend_top_left_two.mirror_x()
    bend_top_left_two.connect('o1', straight_delta_l_left.ports['o2'])

    bend_bottom_left_two = component << bend_90
    bend_bottom_left_two.connect('o1', bend_bottom_left_one.ports['o2'])

    heater = straight_heater = component << straight_heater
    heater.connect('o1', bend_top_left_two['o2'])

    non_heater = component << straight_non_heater
    non_heater.connect('o1', bend_bottom_left_two['o2'])

    bend_top_right_one = component << bend_90
    bend_top_right_one.mirror_x()
    bend_top_right_one.connect('o1', heater.ports['o2'])

    straight_delta_l_right = component << straight_delta_l
    straight_delta_l_right.connect('o1', bend_top_right_one.ports['o2'])

    bend_top_right_two = component << bend_90
    bend_top_right_two.connect('o1', straight_delta_l_right.ports['o2'])

    bend_bottom_right_one = component << bend_90
    bend_bottom_right_one.connect('o1', non_heater.ports['o2'])

    bend_bottom_right_two = component << bend_90
    bend_bottom_right_two.mirror_y()
    bend_bottom_right_two.connect('o1', bend_bottom_right_one.ports['o2'])

    coupler_right = component << coupler
    coupler_right.connect('o2', bend_bottom_right_one['o2'])
    coupler_right.connect('o1', bend_bottom_right_two['o2'])

    #adding pcell ports

    #optical ports

    component.add_port(
        "o1", 
        port=coupler_left.ports["o1"],
        orientation=0
    )
    component.add_label(
        text="o1", 
        position=(
            component.ports["o1"].x,
            component.ports["o1"].y
        ),
    )

    component.add_port(
        "o2",
        port=coupler_left.ports["o2"],
        orientation=0
    )
    component.add_label(
        text="o2", 
        position=(
            component.ports["o2"].x,
            component.ports["o2"].y
        ),
    )

    component.add_port(
        "o3",
        port=coupler_right.ports["o3"],
        orientation=180
    )
    component.add_label(
        text="o3", 
        position=(
            component.ports["o3"].x,
            component.ports["o3"].y
        ),
    )

    component.add_port(
        "o4", 
        port=coupler_right.ports["o4"],
        orientation=180
    )
    component.add_label(
        text="o4", 
        position=(
            component.ports["o4"].x,
            component.ports["o4"].y
        ),
    )

    #electrical ports (heater)

    component.add_port("l_e1", port=heater.ports["l_e1"])
    component.add_label(
        text="l_e1", 
        position=(
            component.ports["l_e1"].x,
            component.ports["l_e1"].y
        ),
    )

    component.add_port("l_e2", port=heater.ports["l_e2"])
    component.add_label(
        text="l_e2", 
        position=(
            component.ports["l_e2"].x,
            component.ports["l_e2"].y
        ),
    )

    component.add_port("l_e3", port=heater.ports["l_e3"])
    component.add_label(
        text="l_e3", 
        position=(
            component.ports["l_e3"].x,
            component.ports["l_e3"].y
        ),
    )

    component.add_port("l_e4", port=heater.ports["l_e4"])
    component.add_label(
        text="l_e4", 
        position=(
            component.ports["l_e4"].x,
            component.ports["l_e4"].y
        ),
    )

    component.add_port("r_e1", port=heater.ports["r_e1"])
    component.add_label(
        text="r_e1", 
        position=(
            component.ports["r_e1"].x,
            component.ports["r_e1"].y
        ),
    )

    component.add_port("r_e2", port=heater.ports["r_e2"])
    component.add_label(
        text="r_e2", 
        position=(
            component.ports["r_e2"].x,
            component.ports["r_e2"].y
        ),
    )

    component.add_port("r_e3", port=heater.ports["r_e3"])
    component.add_label(
        text="r_e3", 
        position=(
            component.ports["r_e3"].x,
            component.ports["r_e3"].y
        ),
    )

    component.add_port("r_e4", port=heater.ports["r_e4"])
    component.add_label(
        text="r_e4", 
        position=(
            component.ports["r_e4"].x,
            component.ports["r_e4"].y
        ),
    )

    return component
