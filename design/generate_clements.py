import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lib.mzi import mzi
import gdsfactory as gf

if __name__ == "__main__":

    MATRIX_SIZE = 8
    HEATER_PADDING = 6
    MZI_SPACE = 20
    
    component = gf.Component("ClementsMesh")
    mzi_component = mzi(padding=6)

    # Get bbox dimensions once for consistent calculations
    mzi_width = mzi_component.dxsize
    mzi_height = mzi_component.dysize

    # First phase: Place all MZI instances
    for column in range(MATRIX_SIZE):
        
        x_pos = column * (mzi_width + MZI_SPACE)

        if column % 2 == 0:
            # Even columns
            num_rows = MATRIX_SIZE // 2
            for row in range(num_rows):
                ref = component.add_ref(mzi_component)
                y_pos = -row * (mzi_height + MZI_SPACE)
                ref.move((x_pos, y_pos))
                ref.name = f'MZI_{column}_{row}'
                print(f"Placed ({ref.name}) at column {column}, row {row} -> ({x_pos}, {y_pos})")

        else:
            # Odd columns
            num_rows = (MATRIX_SIZE // 2) - 1
            for row in range(num_rows):
                ref = component.add_ref(mzi_component)
                y_pos = -(row * (mzi_height + MZI_SPACE) + mzi_height * 0.5 + MZI_SPACE / 2)
                ref.move((x_pos, y_pos))
                ref.name = f'MZI_{column}_{row}'
                print(f"Placed ({ref.name}) at column {column}, row {row} -> ({x_pos}, {y_pos})")

    # Second phase: Connect the instances
    for column in range(1, MATRIX_SIZE):
        
        if column % 2 == 0:
            # Even column connections
            for row in range(MATRIX_SIZE // 2):
                current_mzi = component.insts[f'MZI_{column}_{row}']

                # Previous even upper MZI
                prev_mzi_even = component.insts[f'MZI_{column-2}_{row}']

                # Previous upper odd MZI
                if row < (MATRIX_SIZE // 2) - 1:
                    prev_mzi_odd = component.insts[f'MZI_{column-1}_{row}']

                if row == 0:
                    gf.routing.route_single(
                        component=component,
                        port1=prev_mzi_even.ports['o3'],
                        port2=current_mzi.ports['o2'],
                        cross_section="strip"
                    )
                    gf.routing.route_single(
                        component=component,
                        port1=prev_mzi_odd.ports['o3'],
                        port2=current_mzi.ports['o1'],
                        cross_section="strip"
                    )
                elif row == (MATRIX_SIZE // 2) - 1:
                    gf.routing.route_single(
                        component=component,
                        port1=prev_mzi_even.ports['o4'],
                        port2=current_mzi.ports['o1'],
                        cross_section="strip"
                    )
                    gf.routing.route_single(
                        component=component,
                        port1=prev_mzi_odd.ports['o4'],
                        port2=current_mzi.ports['o2'],
                        cross_section="strip"
                    )

                else:
                    prev_mzi_odd_upper = component.insts[f'MZI_{column-1}_{row-1}']

                    gf.routing.route_single(
                        component=component,
                        port1=prev_mzi_odd.ports['o3'],
                        port2=current_mzi.ports['o1'],
                        cross_section="strip"
                    )

                    gf.routing.route_single(
                        component=component,
                        port1=prev_mzi_odd_upper.ports['o4'],
                        port2=current_mzi.ports['o2'],
                        cross_section="strip"
                    )

        else:

            # Odd column connections
            for row in range((MATRIX_SIZE // 2) - 1):
                current_mzi = component.insts[f'MZI_{column}_{row}']
                
                # Each MZI in odd column connects to two MZIs in previous even column
                upper_prev_mzi = component.insts[f'MZI_{column-1}_{row}']
                lower_prev_mzi = component.insts[f'MZI_{column-1}_{row+1}']
                
                # Connect to upper previous MZI
                gf.routing.route_single(
                    component=component,
                    port1=upper_prev_mzi.ports['o4'],
                    port2=current_mzi.ports['o2'],
                    cross_section="strip"
                )
                
                # Connect to lower previous MZI
                gf.routing.route_single(
                    component=component,
                    port1=lower_prev_mzi.ports['o3'],
                    port2=current_mzi.ports['o1'],
                    cross_section="strip"
                )

    print(f'Total instances count: {len(component.insts)}')
    component.show()