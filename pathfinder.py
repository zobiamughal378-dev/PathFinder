"""
AI Pathfinder - Uninformed Search Algorithms Visualization
Implements: BFS, DFS, UCS, DLS, IDDFS, Bidirectional Search
with Dynamic Obstacle Handling
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from collections import deque
import heapq
import random
from copy import deepcopy

class GridEnvironment:
    """Grid environment with dynamic obstacle support"""
    
    def __init__(self, size=(10, 10), start=(0, 0), target=(9, 9), 
                 obstacle_prob=0.02, dynamic_prob=0.01):
        self.size = size
        self.start = start
        self.target = target
        self.obstacle_prob = obstacle_prob
        self.dynamic_prob = dynamic_prob
        self.grid = np.zeros(size)
        self.static_obstacles = set()
        self.dynamic_obstacles = set()
        
    def add_static_obstacles(self, obstacles):
        """Add static walls to the grid"""
        for obs in obstacles:
            if obs != self.start and obs != self.target:
                self.static_obstacles.add(obs)
                self.grid[obs[0], obs[1]] = 1
    
    def spawn_dynamic_obstacle(self):
        """Randomly spawn a dynamic obstacle"""
        if random.random() < self.dynamic_prob:
            empty_cells = []
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if (i, j) not in self.static_obstacles and \
                       (i, j) not in self.dynamic_obstacles and \
                       (i, j) != self.start and (i, j) != self.target:
                        empty_cells.append((i, j))
            
            if empty_cells:
                new_obs = random.choice(empty_cells)
                self.dynamic_obstacles.add(new_obs)
                self.grid[new_obs[0], new_obs[1]] = 1
                return new_obs
        return None
    
    def is_valid(self, pos):
        """Check if position is valid and not blocked"""
        row, col = pos
        if row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]:
            return False
        if pos in self.static_obstacles or pos in self.dynamic_obstacles:
            return False
        return True
    
    def get_neighbors(self, pos):
        """Get valid neighbors in clockwise order with all diagonals"""
        row, col = pos
        # Order: Up, Top-Right, Right, Bottom-Right, Bottom, Bottom-Left, Left, Top-Left
        directions = [
            (-1, 0),   # Up
            (-1, 1),   # Top-Right
            (0, 1),    # Right
            (1, 1),    # Bottom-Right
            (1, 0),    # Bottom
            (1, -1),   # Bottom-Left
            (0, -1),   # Left
            (-1, -1)   # Top-Left
        ]
        
        neighbors = []
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        
        return neighbors
    
    def get_cost(self, from_pos, to_pos):
        """Get cost of moving from one position to another"""
        # Diagonal moves cost sqrt(2), orthogonal moves cost 1
        if abs(from_pos[0] - to_pos[0]) + abs(from_pos[1] - to_pos[1]) == 2:
            return 1.414  # sqrt(2)
        return 1.0


class PathfinderVisualizer:
    """Visualization class for pathfinding algorithms"""
    
    def __init__(self, env, algorithm_name):
        self.env = env
        self.algorithm_name = algorithm_name
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.canvas.manager.set_window_title("GOOD PERFORMANCE TIME APP")
        
        # Colors
        self.colors = {
            'empty': 'white',
            'wall': 'black',
            'start': 'blue',
            'target': 'green',
            'frontier': 'yellow',
            'explored': 'lightblue',
            'path': 'red',
            'dynamic_obstacle': 'orange'
        }
        
        self.history = []  # Store visualization states
        
    def add_state(self, frontier, explored, path=None, dynamic_obs=None):
        """Add a state to visualization history"""
        state = {
            'frontier': set(frontier) if frontier else set(),
            'explored': set(explored) if explored else set(),
            'path': list(path) if path else [],
            'dynamic_obs': dynamic_obs
        }
        self.history.append(state)
    
    def draw_grid(self, state_idx=None):
        """Draw the current state of the grid"""
        self.ax.clear()
        self.ax.set_xlim(-0.5, self.env.size[1] - 0.5)
        self.ax.set_ylim(-0.5, self.env.size[0] - 0.5)
        self.ax.set_aspect('equal')
        self.ax.set_title(f'{self.algorithm_name}\nGOOD PERFORMANCE TIME APP', 
                         fontsize=16, fontweight='bold')
        
        # Get current state
        if state_idx is not None and state_idx < len(self.history):
            state = self.history[state_idx]
        else:
            state = {'frontier': set(), 'explored': set(), 'path': []}
        
        # Draw grid cells
        for i in range(self.env.size[0]):
            for j in range(self.env.size[1]):
                pos = (i, j)
                
                # Determine cell color
                if pos == self.env.start:
                    color = self.colors['start']
                    self.ax.text(j, i, 'S', ha='center', va='center', 
                               fontsize=12, fontweight='bold', color='white')
                elif pos == self.env.target:
                    color = self.colors['target']
                    self.ax.text(j, i, 'T', ha='center', va='center', 
                               fontsize=12, fontweight='bold', color='white')
                elif pos in self.env.static_obstacles:
                    color = self.colors['wall']
                elif pos in self.env.dynamic_obstacles:
                    color = self.colors['dynamic_obstacle']
                elif pos in state['path']:
                    color = self.colors['path']
                elif pos in state['explored']:
                    color = self.colors['explored']
                elif pos in state['frontier']:
                    color = self.colors['frontier']
                else:
                    color = self.colors['empty']
                
                rect = patches.Rectangle((j - 0.45, i - 0.45), 0.9, 0.9,
                                        linewidth=1, edgecolor='gray',
                                        facecolor=color)
                self.ax.add_patch(rect)
        
        # Add grid lines
        for i in range(self.env.size[0] + 1):
            self.ax.axhline(i - 0.5, color='gray', linewidth=0.5)
        for j in range(self.env.size[1] + 1):
            self.ax.axvline(j - 0.5, color='gray', linewidth=0.5)
        
        # Invert y-axis so (0,0) is at top-left
        self.ax.invert_yaxis()
        
        # Add legend
        legend_elements = [
            patches.Patch(color=self.colors['start'], label='Start'),
            patches.Patch(color=self.colors['target'], label='Target'),
            patches.Patch(color=self.colors['wall'], label='Wall'),
            patches.Patch(color=self.colors['frontier'], label='Frontier'),
            patches.Patch(color=self.colors['explored'], label='Explored'),
            patches.Patch(color=self.colors['path'], label='Path'),
            patches.Patch(color=self.colors['dynamic_obstacle'], label='Dynamic Obstacle')
        ]
        self.ax.legend(handles=legend_elements, loc='upper left', 
                      bbox_to_anchor=(1.02, 1))
        
        plt.tight_layout()
    
    def animate(self, delay=100):
        """Animate the search process"""
        def update(frame):
            self.draw_grid(frame)
            return self.ax,
        
        anim = FuncAnimation(self.fig, update, frames=len(self.history),
                           interval=delay, repeat=False, blit=False)
        plt.show()
        return anim
    
    def show_final(self):
        """Show final result"""
        if self.history:
            self.draw_grid(len(self.history) - 1)
        else:
            self.draw_grid()
        plt.show()


class SearchAlgorithms:
    """Implementation of all uninformed search algorithms"""
    
    def __init__(self, env, visualizer):
        self.env = env
        self.viz = visualizer
        self.path_found = False
        self.steps = 0
        
    def reconstruct_path(self, came_from, current):
        """Reconstruct path from came_from dictionary"""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(self.env.start)
        return path[::-1]
    
    def bfs(self):
        """Breadth-First Search"""
        print("Running BFS...")
        frontier = deque([self.env.start])
        came_from = {}
        explored = set()
        
        while frontier:
            # Check for dynamic obstacle
            new_obs = self.env.spawn_dynamic_obstacle()
            
            current = frontier.popleft()
            
            if current == self.env.target:
                path = self.reconstruct_path(came_from, current)
                self.viz.add_state(frontier, explored, path)
                print(f"BFS: Path found in {self.steps} steps!")
                return path
            
            if current in explored:
                continue
                
            explored.add(current)
            self.steps += 1
            
            for neighbor in self.env.get_neighbors(current):
                if neighbor not in explored and neighbor not in frontier:
                    frontier.append(neighbor)
                    came_from[neighbor] = current
            
            # Visualize current state
            self.viz.add_state(list(frontier), explored, dynamic_obs=new_obs)
        
        print("BFS: No path found!")
        return None
    
    def dfs(self):
        """Depth-First Search"""
        print("Running DFS...")
        frontier = [self.env.start]
        came_from = {}
        explored = set()
        
        while frontier:
            # Check for dynamic obstacle
            new_obs = self.env.spawn_dynamic_obstacle()
            
            current = frontier.pop()
            
            if current == self.env.target:
                path = self.reconstruct_path(came_from, current)
                self.viz.add_state(frontier, explored, path)
                print(f"DFS: Path found in {self.steps} steps!")
                return path
            
            if current in explored:
                continue
                
            explored.add(current)
            self.steps += 1
            
            # Add neighbors in reverse order for DFS
            neighbors = self.env.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in explored and neighbor not in frontier:
                    frontier.append(neighbor)
                    came_from[neighbor] = current
            
            # Visualize current state
            self.viz.add_state(list(frontier), explored, dynamic_obs=new_obs)
        
        print("DFS: No path found!")
        return None
    
    def ucs(self):
        """Uniform-Cost Search"""
        print("Running UCS...")
        frontier = [(0, self.env.start)]
        came_from = {}
        cost_so_far = {self.env.start: 0}
        explored = set()
        
        while frontier:
            # Check for dynamic obstacle
            new_obs = self.env.spawn_dynamic_obstacle()
            
            current_cost, current = heapq.heappop(frontier)
            
            if current == self.env.target:
                path = self.reconstruct_path(came_from, current)
                self.viz.add_state([x[1] for x in frontier], explored, path)
                print(f"UCS: Path found in {self.steps} steps with cost {current_cost:.2f}!")
                return path
            
            if current in explored:
                continue
                
            explored.add(current)
            self.steps += 1
            
            for neighbor in self.env.get_neighbors(current):
                new_cost = cost_so_far[current] + self.env.get_cost(current, neighbor)
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current
            
            # Visualize current state
            self.viz.add_state([x[1] for x in frontier], explored, dynamic_obs=new_obs)
        
        print("UCS: No path found!")
        return None
    
    def dls(self, depth_limit=10):
        """Depth-Limited Search"""
        print(f"Running DLS with depth limit {depth_limit}...")
        
        def dls_recursive(node, depth, came_from, explored, frontier_set):
            if depth == 0:
                return None
            
            # Check for dynamic obstacle
            new_obs = self.env.spawn_dynamic_obstacle()
            
            if node == self.env.target:
                return self.reconstruct_path(came_from, node)
            
            explored.add(node)
            self.steps += 1
            
            for neighbor in self.env.get_neighbors(node):
                if neighbor not in explored:
                    frontier_set.add(neighbor)
                    came_from[neighbor] = node
                    
                    # Visualize
                    self.viz.add_state(list(frontier_set), explored, dynamic_obs=new_obs)
                    
                    result = dls_recursive(neighbor, depth - 1, came_from, 
                                          explored, frontier_set)
                    if result is not None:
                        return result
                    
                    frontier_set.discard(neighbor)
            
            return None
        
        came_from = {}
        explored = set()
        frontier_set = set([self.env.start])
        
        result = dls_recursive(self.env.start, depth_limit, came_from, 
                              explored, frontier_set)
        
        if result:
            print(f"DLS: Path found in {self.steps} steps!")
        else:
            print(f"DLS: No path found within depth limit {depth_limit}!")
        
        return result
    
    def iddfs(self, max_depth=20):
        """Iterative Deepening DFS"""
        print(f"Running IDDFS with max depth {max_depth}...")
        
        for depth in range(1, max_depth + 1):
            print(f"  Trying depth {depth}...")
            self.steps = 0
            
            # Reset for each iteration
            came_from = {}
            explored = set()
            frontier_set = set([self.env.start])
            
            def iddfs_recursive(node, current_depth):
                if current_depth == 0:
                    return None
                
                # Check for dynamic obstacle
                new_obs = self.env.spawn_dynamic_obstacle()
                
                if node == self.env.target:
                    return self.reconstruct_path(came_from, node)
                
                explored.add(node)
                self.steps += 1
                
                for neighbor in self.env.get_neighbors(node):
                    if neighbor not in explored:
                        frontier_set.add(neighbor)
                        came_from[neighbor] = node
                        
                        # Visualize
                        self.viz.add_state(list(frontier_set), explored, 
                                         dynamic_obs=new_obs)
                        
                        result = iddfs_recursive(neighbor, current_depth - 1)
                        if result is not None:
                            return result
                        
                        frontier_set.discard(neighbor)
                
                return None
            
            result = iddfs_recursive(self.env.start, depth)
            
            if result:
                print(f"IDDFS: Path found at depth {depth} in {self.steps} steps!")
                return result
        
        print(f"IDDFS: No path found within max depth {max_depth}!")
        return None
    
    def bidirectional_search(self):
        """Bidirectional Search"""
        print("Running Bidirectional Search...")
        
        # Forward search from start
        frontier_forward = deque([self.env.start])
        came_from_forward = {}
        explored_forward = set()
        
        # Backward search from target
        frontier_backward = deque([self.env.target])
        came_from_backward = {}
        explored_backward = set()
        
        while frontier_forward and frontier_backward:
            # Check for dynamic obstacle
            new_obs = self.env.spawn_dynamic_obstacle()
            
            # Forward step
            if frontier_forward:
                current_forward = frontier_forward.popleft()
                
                if current_forward in explored_backward:
                    # Found intersection!
                    path_forward = self.reconstruct_path(came_from_forward, 
                                                        current_forward)
                    path_backward = []
                    node = current_forward
                    while node in came_from_backward:
                        node = came_from_backward[node]
                        path_backward.append(node)
                    
                    path = path_forward + path_backward
                    self.viz.add_state(
                        list(frontier_forward) + list(frontier_backward),
                        explored_forward | explored_backward,
                        path
                    )
                    print(f"Bidirectional: Path found in {self.steps} steps!")
                    return path
                
                if current_forward not in explored_forward:
                    explored_forward.add(current_forward)
                    self.steps += 1
                    
                    for neighbor in self.env.get_neighbors(current_forward):
                        if neighbor not in explored_forward:
                            frontier_forward.append(neighbor)
                            came_from_forward[neighbor] = current_forward
            
            # Backward step
            if frontier_backward:
                current_backward = frontier_backward.popleft()
                
                if current_backward in explored_forward:
                    # Found intersection!
                    path_forward = self.reconstruct_path(came_from_forward, 
                                                        current_backward)
                    path_backward = []
                    node = current_backward
                    while node in came_from_backward:
                        node = came_from_backward[node]
                        path_backward.append(node)
                    
                    path = path_forward + path_backward
                    self.viz.add_state(
                        list(frontier_forward) + list(frontier_backward),
                        explored_forward | explored_backward,
                        path
                    )
                    print(f"Bidirectional: Path found in {self.steps} steps!")
                    return path
                
                if current_backward not in explored_backward:
                    explored_backward.add(current_backward)
                    self.steps += 1
                    
                    for neighbor in self.env.get_neighbors(current_backward):
                        if neighbor not in explored_backward:
                            frontier_backward.append(neighbor)
                            came_from_backward[neighbor] = current_backward
            
            # Visualize current state
            self.viz.add_state(
                list(frontier_forward) + list(frontier_backward),
                explored_forward | explored_backward,
                dynamic_obs=new_obs
            )
        
        print("Bidirectional: No path found!")
        return None


def create_sample_environment(scenario='best'):
    """Create sample environments for testing"""
    env = GridEnvironment(size=(10, 10), start=(0, 0), target=(9, 9), 
                         obstacle_prob=0.02, dynamic_prob=0.005)
    
    if scenario == 'best':
        # Best case: Direct path with minimal obstacles
        obstacles = [(5, i) for i in range(3, 7)]
        env.add_static_obstacles(obstacles)
    elif scenario == 'worst':
        # Worst case: Complex maze
        obstacles = []
        # Create a maze-like structure
        for i in range(2, 8):
            obstacles.append((i, 3))
            obstacles.append((i, 7))
        for j in range(1, 9):
            if j != 5:
                obstacles.append((2, j))
                obstacles.append((7, j))
        env.add_static_obstacles(obstacles)
    else:
        # Medium case
        obstacles = [(i, 5) for i in range(1, 9) if i != 4]
        env.add_static_obstacles(obstacles)
    
    return env


def main():
    """Main execution function"""
    print("=" * 60)
    print("AI PATHFINDER - Uninformed Search Algorithms")
    print("GOOD PERFORMANCE TIME APP")
    print("=" * 60)
    
    # Get user choice
    print("\nSelect scenario:")
    print("1. Best Case (Direct path)")
    print("2. Worst Case (Complex maze)")
    print("3. Medium Case")
    
    choice = input("Enter choice (1-3): ").strip()
    scenario_map = {'1': 'best', '2': 'worst', '3': 'medium'}
    scenario = scenario_map.get(choice, 'best')
    
    print("\nSelect algorithm:")
    print("1. BFS (Breadth-First Search)")
    print("2. DFS (Depth-First Search)")
    print("3. UCS (Uniform-Cost Search)")
    print("4. DLS (Depth-Limited Search)")
    print("5. IDDFS (Iterative Deepening DFS)")
    print("6. Bidirectional Search")
    print("7. Run All Algorithms")
    
    algo_choice = input("Enter choice (1-7): ").strip()
    
    algorithms = {
        '1': ('BFS', 'bfs'),
        '2': ('DFS', 'dfs'),
        '3': ('UCS', 'ucs'),
        '4': ('DLS', 'dls'),
        '5': ('IDDFS', 'iddfs'),
        '6': ('Bidirectional Search', 'bidirectional_search')
    }
    
    if algo_choice == '7':
        # Run all algorithms
        for key, (name, method) in algorithms.items():
            print(f"\n{'=' * 60}")
            print(f"Running {name}...")
            print('=' * 60)
            
            env = create_sample_environment(scenario)
            viz = PathfinderVisualizer(env, name)
            searcher = SearchAlgorithms(env, viz)
            
            # Run the algorithm
            method_func = getattr(searcher, method)
            path = method_func()
            
            # Show animation
            viz.animate(delay=50)
    else:
        # Run single algorithm
        if algo_choice in algorithms:
            name, method = algorithms[algo_choice]
            
            env = create_sample_environment(scenario)
            viz = PathfinderVisualizer(env, name)
            searcher = SearchAlgorithms(env, viz)
            
            # Run the algorithm
            method_func = getattr(searcher, method)
            path = method_func()
            
            # Show animation
            viz.animate(delay=100)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
