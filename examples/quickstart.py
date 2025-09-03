"""
Quick start guide for Minimax performance tools.
"""

from minimax_tools import run_benchmark


def quick_benchmark():
    """Run a quick benchmark with default settings."""
    print("Running quick benchmark...")
    
    # Run benchmark with default tasks
    results = run_benchmark()
    
    # Display results
    print("\nBenchmark Results:")
    for task, data in results.items():
        print(f"  {task}:")
        print(f"    Execution time: {data['execution_time']:.3f}s")
        print(f"    CPU usage: {data['cpu_usage']:.1f}%")
        print(f"    Memory usage: {data['memory_usage']:.1f}%")
        print(f"    Status: {data['status']}")
        print()
    
    return results


if __name__ == "__main__":
    quick_benchmark()
