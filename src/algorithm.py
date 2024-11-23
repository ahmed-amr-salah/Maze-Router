
from collections import deque
from typing import List, Tuple, Optional, Dict
from parser import MazeRouterInput


def lee_maze_algorithm(
    grid: List[List[Dict]], 
    start: Tuple[int, int, int], 
    end: Tuple[int, int, int], 
    penalties: Tuple[int, int]
) -> Optional[List[Tuple[int, int, int]]]:
    bend_penalty, via_penalty = penalties
    queue = deque([start])
    visited = set()
    parent = {}
    visited.add(start)
    
    while queue:
        current = queue.popleft()
        layer, x, y = current
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent.get(current)
            return path[::-1]
        if layer == 1:
            directions = [
                (1, 0, layer),    # Move Right
                (-1, 0, layer),   # Move Left
                (0, 0, 2),         # Switch to Layer 2
                (0, 1, layer),    # Move Up
                (0, -1, layer)    # Move Down
            ]
        elif layer == 2:
            directions = [
                (0, 1, layer),    # Move Up
                (0, -1, layer),   # Move Down
                (0, 0, 1),         # Switch to Layer 1
                (1, 0, layer),    # Move Right
                (-1, 0, layer)    # Move Left
            ]
        else:
            directions = []
        
        for dx, dy, new_layer in directions:
            nx, ny = x + dx, y + dy
            neighbor = (new_layer, nx, ny)
            
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if neighbor not in visited and not grid[ny][nx]['obstacle']:
                    cost = grid[y][x].get('cost', 0)
                    if layer != new_layer:
                        cost += via_penalty
                    if (layer==1 and dy!=0) or (layer==2 and dx!=0):
                        cost += bend_penalty
                    grid[ny][nx]['cost'] = cost
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
    return None

def route_net(
    grid: List[List[Dict]], 
    net: Dict, 
    penalties: Tuple[int, int]
) -> Optional[List[Tuple[int, int, int]]]:
    pins = net['pins']
    if len(pins) < 2:
        raise ValueError(f"Net '{net['name']}' does not have enough pins to route.")
    
    full_path = []
    
    for i in range(len(pins) - 1):
        start_pin = pins[i]
        end_pin = pins[i + 1]
        start = (start_pin['layer'], start_pin['x'], start_pin['y'])
        end = (end_pin['layer'], end_pin['x'], end_pin['y'])
        
        path_segment = lee_maze_algorithm(grid, start, end, penalties)
        if path_segment is None:
            return None
        
        if i > 0:
            path_segment = path_segment[1:]
        
        full_path.extend(path_segment)
    
    return full_path

def route_all_nets(
    router_input: MazeRouterInput
) -> Dict[str, List[Tuple[int, int, int]]]:
    grid = [
        [{'obstacle': False} for _ in range(router_input.grid_width)]
        for _ in range(router_input.grid_height)
    ]
    
    for obs in router_input.obstructions:
        layer, x, y = obs
        if 0 <= x < router_input.grid_width and 0 <= y < router_input.grid_height:
            grid[y][x]['obstacle'] = True
    
    routing_results = {}
    penalties = (router_input.bend_penalty, router_input.via_penalty)
    
    for net in router_input.nets:
        path = route_net(grid, net, penalties)  # Pass net dictionary
        if path:
            routing_results[net['name']] = path  # Access net name
    
    return routing_results
