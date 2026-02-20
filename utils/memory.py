"""
Memory monitoring and optimization utilities.
"""

import psutil
import gc
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def get_memory_usage() -> Dict[str, float]:
    """
    Get current memory usage statistics.
    
    Returns:
        Dictionary with memory metrics in MB
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    
    return {
        "rss_mb": memory_info.rss / 1024 / 1024,  # Resident Set Size
        "vms_mb": memory_info.vms / 1024 / 1024,  # Virtual Memory Size
        "percent": process.memory_percent()
    }


def log_memory_usage(context: str = ""):
    """Log current memory usage with context."""
    stats = get_memory_usage()
    logger.info(
        f"Memory Usage {context}: "
        f"RSS={stats['rss_mb']:.2f}MB, "
        f"VMS={stats['vms_mb']:.2f}MB, "
        f"Percent={stats['percent']:.2f}%"
    )


def force_garbage_collection():
    """Force garbage collection to free memory."""
    collected = gc.collect()
    logger.info(f"Garbage collection freed {collected} objects")
    return collected


def check_memory_threshold(threshold_mb: float = 450) -> bool:
    """
    Check if memory usage exceeds threshold.
    
    Args:
        threshold_mb: Memory threshold in MB
        
    Returns:
        True if memory usage is below threshold
    """
    stats = get_memory_usage()
    is_safe = stats["rss_mb"] < threshold_mb
    
    if not is_safe:
        logger.warning(
            f"Memory threshold exceeded: {stats['rss_mb']:.2f}MB > {threshold_mb}MB"
        )
    
    return is_safe


class MemoryMonitor:
    """Context manager for monitoring memory usage."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_memory = None
    
    def __enter__(self):
        self.start_memory = get_memory_usage()
        log_memory_usage(f"[START] {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_memory = get_memory_usage()
        delta = end_memory["rss_mb"] - self.start_memory["rss_mb"]
        
        logger.info(
            f"[END] {self.operation_name}: "
            f"Memory delta = {delta:+.2f}MB"
        )
        
        log_memory_usage(f"[END] {self.operation_name}")
