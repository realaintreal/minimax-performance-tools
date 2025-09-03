"""
Comprehensive demonstration of Minimax performance tools.
"""

import time
import json
from minimax_tools import (
    run_benchmark,
    measure_latency,
    analyze_resources,
    setup_environment,
    collect_metrics,
    generate_report
)


def main():
    """Run comprehensive performance demonstration."""
    print("=== Minimax Performance Tools Demo ===\n")
    
    # Set up environment
    print("1. Setting up benchmark environment...")
    output_dir = setup_environment("./demo_results")
    print(f"   Environment ready at: {output_dir}")
    
    # Run basic benchmarks
    print("\n2. Running performance benchmarks...")
    benchmark_results = run_benchmark()
    print(f"   Completed {len(benchmark_results)} benchmark tasks")
    
    # Measure latency
    print("\n3. Measuring model latency...")
    latency_results = measure_latency()
    print(f"   Average latency: {latency_results['mean_latency']:.3f}s")
    
    # Analyze resources (shortened for demo)
    print("\n4. Analyzing resource utilization...")
    resource_results = analyze_resources(duration=10)
    print(f"   Monitoring completed for {resource_results['monitoring_duration']}s")
    
    # Collect metrics
    print("\n5. Collecting system metrics...")
    system_metrics = collect_metrics("system")
    process_metrics = collect_metrics("process")
    print("   Metrics collected successfully")
    
    # Generate comprehensive report
    print("\n6. Generating performance report...")
    all_results = {
        "benchmark_results": benchmark_results,
        "latency_results": latency_results,
        "resource_results": resource_results,
        "system_metrics": system_metrics,
        "process_metrics": process_metrics
    }
    
    report_path = f"{output_dir}/reports/demo_report.json"
    generate_report(all_results, report_path)
    print(f"   Report saved to: {report_path}")
    
    # Display summary
    print("\n=== Demo Summary ===")
    print(f"Tasks benchmarked: {len(benchmark_results)}")
    print(f"Average latency: {latency_results['mean_latency']:.3f}s")
    print(f"Peak CPU usage: {resource_results['cpu_usage']['max']:.1f}%")
    print(f"Peak memory usage: {resource_results['memory_usage']['max']:.1f}%")
    print(f"\nDetailed results saved to: {output_dir}")


if __name__ == "__main__":
    main()
