"""
Utility functions for Minimax performance tools.
"""

import os
import json
import time
import psutil
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime


def setup_environment(output_dir: str = "./benchmark_results") -> str:
    """
    Set up the benchmarking environment.
    
    Args:
        output_dir: Directory to store benchmark results
        
    Returns:
        Path to the created output directory
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subdirectories
    subdirs = ["raw_data", "processed_data", "reports", "plots"]
    for subdir in subdirs:
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
    
    # Initialize environment config
    config = {
        "created_at": datetime.now().isoformat(),
        "output_directory": output_dir,
        "subdirectories": subdirs,
        "system_info": {
            "platform": os.name,
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total
        }
    }
    
    # Save config
    config_path = os.path.join(output_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return output_dir


def collect_metrics(metrics_type: str = "system") -> Dict[str, Any]:
    """
    Collect various performance metrics.
    
    Args:
        metrics_type: Type of metrics to collect ("system", "process", "network")
        
    Returns:
        Dictionary containing collected metrics
    """
    timestamp = datetime.now().isoformat()
    
    if metrics_type == "system":
        return {
            "timestamp": timestamp,
            "type": "system",
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
        }
    
    elif metrics_type == "process":
        process = psutil.Process()
        return {
            "timestamp": timestamp,
            "type": "process",
            "cpu_percent": process.cpu_percent(),
            "memory_percent": process.memory_percent(),
            "num_threads": process.num_threads(),
            "open_files": len(process.open_files())
        }
    
    elif metrics_type == "network":
        net_io = psutil.net_io_counters()
        return {
            "timestamp": timestamp,
            "type": "network",
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    else:
        raise ValueError(f"Unknown metrics type: {metrics_type}")


def generate_report(results: Dict[str, Any], output_path: str) -> None:
    """
    Generate a comprehensive performance report.
    
    Args:
        results: Benchmark results dictionary
        output_path: Path to save the report
    """
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": _generate_summary(results),
        "detailed_results": results,
        "recommendations": _generate_recommendations(results)
    }
    
    # Save as JSON
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Also save as CSV for easier analysis
    if "benchmark_results" in results:
        df = pd.DataFrame(results["benchmark_results"])
        csv_path = output_path.replace('.json', '.csv')
        df.to_csv(csv_path, index=False)


def _generate_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a summary of the benchmark results."""
    summary = {
        "total_tasks": 0,
        "completed_tasks": 0,
        "failed_tasks": 0,
        "average_execution_time": 0,
        "peak_memory_usage": 0
    }
    
    if "benchmark_results" in results:
        benchmark_data = results["benchmark_results"]
        summary["total_tasks"] = len(benchmark_data)
        summary["completed_tasks"] = sum(1 for task in benchmark_data.values() 
                                       if task.get("status") == "completed")
        summary["failed_tasks"] = summary["total_tasks"] - summary["completed_tasks"]
        
        execution_times = [task.get("execution_time", 0) for task in benchmark_data.values()]
        if execution_times:
            summary["average_execution_time"] = sum(execution_times) / len(execution_times)
        
        memory_usages = [task.get("memory_usage", 0) for task in benchmark_data.values()]
        if memory_usages:
            summary["peak_memory_usage"] = max(memory_usages)
    
    return summary


def _generate_recommendations(results: Dict[str, Any]) -> List[str]:
    """Generate performance improvement recommendations."""
    recommendations = []
    
    if "benchmark_results" in results:
        benchmark_data = results["benchmark_results"]
        
        # Check for high execution times
        slow_tasks = [(name, data) for name, data in benchmark_data.items() 
                     if data.get("execution_time", 0) > 1.0]
        if slow_tasks:
            recommendations.append(f"Consider optimizing slow tasks: {[name for name, _ in slow_tasks]}")
        
        # Check for high memory usage
        high_memory_tasks = [(name, data) for name, data in benchmark_data.items() 
                           if data.get("memory_usage", 0) > 80]
        if high_memory_tasks:
            recommendations.append(f"High memory usage detected in tasks: {[name for name, _ in high_memory_tasks]}")
        
        # Check for failed tasks
        failed_tasks = [name for name, data in benchmark_data.items() 
                       if data.get("status") != "completed"]
        if failed_tasks:
            recommendations.append(f"Failed tasks require attention: {failed_tasks}")
    
    if not recommendations:
        recommendations.append("Performance is within acceptable parameters.")
    
    return recommendations
