
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

def print_routing_result(net_name, path):
    print(f"  Path for net '{net_name}':")
    for step in path:
        layer, x, y = step
        print(f"    Layer {layer} at ({x}, {y})")

def write_routing_results_to_file(routing_results, output_path):
    try:
        with open(output_path, 'w') as f:
            for net_name, path in routing_results.items():
                path_str = ' '.join([f"({layer}, {x}, {y})" for layer, x, y in path])
                f.write(f"{net_name} {path_str}\n")
        print(f"Routing results have been successfully written to '{output_path}'.")
    except IOError as e:
        print(f"Failed to write routing results to '{output_path}': {e}")