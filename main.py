from parser import parse_maze_router_input
from output_display import print_input_data

if __name__ == "__main__":
    try:
        input_path = "input.txt"
        router_input = parse_maze_router_input(input_path)
        print_input_data(router_input)
   

    except Exception as e:
        print(f"Error: {e}")
