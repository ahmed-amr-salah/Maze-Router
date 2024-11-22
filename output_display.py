
#list of all the functions to be used to display the output


def print_input_data(router_input):
    print(f"Grid Dimensions: {router_input.grid_width}x{router_input.grid_height}")
    print(f"Bend Penalty: {router_input.bend_penalty}, Via Penalty: {router_input.via_penalty}")

    print("Obstructions:")
    for obs in router_input.obstructions:
        print(f"  Layer {obs[0]} at ({obs[1]}, {obs[2]})")

    print("Nets:")
    for net in router_input.nets:
        print(f"  {net['name']}:")
        for pin in net['pins']:
            print(f"    Layer {pin['layer']}, ({pin['x']}, {pin['y']})")
