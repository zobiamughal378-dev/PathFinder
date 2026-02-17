"""
Test script to generate screenshots for all algorithms
in both best and worst case scenarios
"""

import matplotlib.pyplot as plt
from pathfinder import (GridEnvironment, PathfinderVisualizer, 
                        SearchAlgorithms, create_sample_environment)
import os

def save_screenshot(env, algorithm_name, method_name, scenario):
    """Run algorithm and save screenshot"""
    print(f"\nGenerating screenshot: {algorithm_name} - {scenario}")
    
    # Create visualizer
    viz = PathfinderVisualizer(env, algorithm_name)
    searcher = SearchAlgorithms(env, viz)
    
    # Run the algorithm
    method_func = getattr(searcher, method_name)
    
    try:
        if method_name == 'dls':
            path = method_func(depth_limit=15)
        elif method_name == 'iddfs':
            path = method_func(max_depth=25)
        else:
            path = method_func()
        
        # Draw final state
        viz.draw_grid(len(viz.history) - 1 if viz.history else None)
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        # Save figure
        filename = f'screenshots/{algorithm_name.lower().replace(" ", "_")}_{scenario}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Saved: {filename}")
        
        # Close figure
        plt.close()
        
        return path is not None
        
    except Exception as e:
        print(f"Error: {e}")
        plt.close()
        return False


def main():
    """Generate all screenshots"""
    print("=" * 70)
    print("GENERATING SCREENSHOTS FOR REPORT")
    print("=" * 70)
    
    algorithms = [
        ('BFS', 'bfs'),
        ('DFS', 'dfs'),
        ('UCS', 'ucs'),
        ('DLS', 'dls'),
        ('IDDFS', 'iddfs'),
        ('Bidirectional Search', 'bidirectional_search')
    ]
    
    scenarios = ['best', 'worst']
    
    results = {}
    
    for scenario in scenarios:
        print(f"\n{'=' * 70}")
        print(f"SCENARIO: {scenario.upper()} CASE")
        print('=' * 70)
        
        for algo_name, method_name in algorithms:
            # Create fresh environment for each test
            env = create_sample_environment(scenario)
            
            # Run and save
            success = save_screenshot(env, algo_name, method_name, scenario)
            
            key = f"{algo_name}_{scenario}"
            results[key] = "✓ Success" if success else "✗ Failed"
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for key, status in results.items():
        print(f"{key:40s} {status}")
    
    print("\nAll screenshots saved in 'screenshots/' directory")
    print("=" * 70)


if __name__ == "__main__":
    main()
