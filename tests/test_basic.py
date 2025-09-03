"""
Basic tests for Minimax performance tools.
"""

import unittest
import time
from unittest.mock import patch, MagicMock
from minimax_tools.benchmark import run_benchmark, measure_latency
from minimax_tools.utils import setup_environment, collect_metrics
from minimax_tools.network_utils import check_network_connectivity, get_network_info


class TestBenchmarkFunctions(unittest.TestCase):
    """Test benchmark-related functions."""
    
    def test_run_benchmark_returns_dict(self):
        """Test that run_benchmark returns a dictionary."""
        results = run_benchmark()
        self.assertIsInstance(results, dict)
        self.assertGreater(len(results), 0)
    
    def test_run_benchmark_with_custom_tasks(self):
        """Test run_benchmark with custom task list."""
        custom_tasks = ["custom_task_1", "custom_task_2"]
        results = run_benchmark(custom_tasks)
        self.assertEqual(len(results), 2)
        self.assertIn("custom_task_1", results)
        self.assertIn("custom_task_2", results)
    
    def test_measure_latency_returns_stats(self):
        """Test that measure_latency returns proper statistics."""
        stats = measure_latency(num_requests=3)
        required_keys = ["mean_latency", "median_latency", "min_latency", "max_latency", "std_latency"]
        for key in required_keys:
            self.assertIn(key, stats)
        self.assertIsInstance(stats["mean_latency"], float)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_setup_environment_creates_directory(self):
        """Test that setup_environment creates the output directory."""
        import tempfile
        import shutil
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = setup_environment(temp_dir)
            self.assertTrue(os.path.exists(output_dir))
            
            # Check subdirectories
            subdirs = ["raw_data", "processed_data", "reports", "plots"]
            for subdir in subdirs:
                self.assertTrue(os.path.exists(os.path.join(output_dir, subdir)))
            
            # Check config file
            config_path = os.path.join(output_dir, "config.json")
            self.assertTrue(os.path.exists(config_path))
    
    def test_collect_metrics_returns_dict(self):
        """Test that collect_metrics returns a dictionary."""
        metrics = collect_metrics("system")
        self.assertIsInstance(metrics, dict)
        self.assertIn("timestamp", metrics)
        self.assertIn("type", metrics)
        self.assertEqual(metrics["type"], "system")
    
    def test_collect_metrics_invalid_type(self):
        """Test collect_metrics with invalid metrics type."""
        with self.assertRaises(ValueError):
            collect_metrics("invalid_type")


class TestNetworkUtils(unittest.TestCase):
    """Test network utility functions."""
    
    @patch('socket.create_connection')
    def test_check_network_connectivity_success(self, mock_create_connection):
        """Test check_network_connectivity with successful connection."""
        mock_create_connection.return_value = MagicMock()
        result = check_network_connectivity()
        self.assertTrue(result)
    
    @patch('socket.create_connection')
    def test_check_network_connectivity_failure(self, mock_create_connection):
        """Test check_network_connectivity with failed connection."""
        mock_create_connection.side_effect = OSError()
        result = check_network_connectivity()
        self.assertFalse(result)
    
    @patch('socket.gethostname')
    @patch('socket.gethostbyname')
    def test_get_network_info(self, mock_gethostbyname, mock_gethostname):
        """Test get_network_info function."""
        mock_gethostname.return_value = "test-host"
        mock_gethostbyname.return_value = "192.168.1.100"
        
        with patch.object(check_network_connectivity, return_value=True):
            info = get_network_info()
            self.assertEqual(info["hostname"], "test-host")
            self.assertEqual(info["local_ip"], "192.168.1.100")
            self.assertTrue(info["connectivity"])


if __name__ == "__main__":
    unittest.main()
