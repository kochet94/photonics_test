import gdsfactory as gf

@gf.cell
def mzi(
    delta_l: float = 10.0,
    wg_width: float = 2.0, 
    bend_radius: float = 10.0, 
    heater_length: float = 40.0
) -> gf.component:
    
    STRAIGHT_CONST_LENGTH = 2.0

    component = gf.Component()
    
    #initializing components

    coupler = gf.components.coupler()
    bend_90 = gf.components.bend_euler(radius=bend_radius)
    straight_const = gf.components.straight(length=STRAIGHT_CONST_LENGTH)
    straight_ref = gf.components.straight(length=STRAIGHT_CONST_LENGTH + delta_l)
    straight_heater = gf.components.straight_heater_metal(length=heater_length)
    straight_non_heater = gf.components.straight(length=heater_length)

    #creating and connecting instances

    coupler_left = component << coupler

    bend_top_left_one = component << bend_90
    bend_top_left_one.connect('o1', coupler_left.ports['o3'])

    bend_bottom_left_one = component << bend_90
    bend_bottom_left_one.mirror_y()
    bend_bottom_left_one.connect('o1', coupler_left.ports['o4'])

    straight_vertical_right_const = component << straight_const
    straight_vertical_right_const.connect('o1', bend_bottom_left_one.ports['o2'])

    straight_vertical_left_ref = component << straight_ref
    straight_vertical_left_ref.connect('o1', bend_top_left_one.ports['o2'])

    bend_top_left_two = component << bend_90
    bend_top_left_two.mirror_x()
    bend_top_left_two.connect('o1', straight_vertical_left_ref.ports['o2'])

    bend_bottom_left_two = component << bend_90
    bend_bottom_left_two.connect('o1', straight_vertical_right_const.ports['o2'])

    heater = straight_heater = component << straight_heater
    heater.connect('o1', bend_top_left_two['o2'])

    non_heater = component << straight_non_heater
    non_heater.connect('o1', bend_bottom_left_two['o2'])

    bend_top_right_one = component << bend_90
    bend_top_right_one.mirror_x()
    bend_top_right_one.connect('o1', heater.ports['o2'])

    straight_vertical_right_ref = component << straight_ref
    straight_vertical_right_ref.connect('o1', bend_top_right_one.ports['o2'])

    bend_top_right_two = component << bend_90
    bend_top_right_two.connect('o1', straight_vertical_right_ref.ports['o2'])

    bend_bottom_right_one = component << bend_90
    bend_bottom_right_one.connect('o1', non_heater.ports['o2'])

    straight_vertical_right_const = component << straight_const
    straight_vertical_right_const.connect('o1', bend_bottom_right_one.ports['o2'])

    bend_bottom_right_two = component << bend_90
    bend_bottom_right_two.mirror_y()
    bend_bottom_right_two.connect('o1', straight_vertical_right_const.ports['o2'])

    coupler_right = component << coupler
    coupler_right.connect('o2', bend_bottom_right_one['o2'])
    coupler_right.connect('o1', bend_bottom_right_two['o2'])

    #adding pcell ports

    #optical ports

    component.add_port("o1", port=coupler_left.ports["o1"])
    component.add_port("o2", port=coupler_left.ports["o2"])
    component.add_port("o3", port=coupler_right.ports["o3"])
    component.add_port("o4", port=coupler_right.ports["o4"])

    #electrical ports (heater)

    component.add_port("e1", port=heater.ports["l_e1"])
    component.add_port("e2", port=heater.ports["r_e1"])

    return component

if __name__ == '__main__':
    gradient_mzi = mzi()
    mzi().show()
