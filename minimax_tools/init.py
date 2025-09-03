"""
Minimax Performance Tools

A comprehensive benchmarking and performance analysis toolkit for Minimax AI agents.
"""

__version__ = "0.1.0"
__author__ = "AI Performance Research Team"
__email__ = "research@example.com"

from .benchmark import run_benchmark, measure_latency, analyze_resources
from .utils import setup_environment, collect_metrics, generate_report

__all__ = [
    "run_benchmark",
    "measure_latency", 
    "analyze_resources",
    "setup_environment",
    "collect_metrics",
    "generate_report",
]
