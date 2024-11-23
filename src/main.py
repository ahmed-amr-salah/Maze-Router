import sys
from parser import parse_maze_router_input
from output_display import print_input_data
from algorithm import route_all_nets
from output_display import print_routing_result, write_routing_results_to_file

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            print("Usage: python main.py <input_path> <output_path>")
            sys.exit(1)
        
        input_path = sys.argv[1]
        output_path = sys.argv[2]

        router_input = parse_maze_router_input(input_path)
        print_input_data(router_input)
        routing_results = route_all_nets(router_input)

        for net_name, path in routing_results.items():
            print_routing_result(net_name, path)
        
        write_routing_results_to_file(routing_results, output_path)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
