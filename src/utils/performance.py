import time
import logging
import threading
from typing import Dict, Any, Optional, Callable
from functools import wraps
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Container for performance metrics."""
    name: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None

class PerformanceMonitor:
    """Performance monitoring and optimization utility."""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics: deque = deque(maxlen=max_history)
        self.lock = threading.Lock()
        self.enabled = True
        
        # Performance thresholds
        self.slow_threshold = 1.0  # seconds
        self.critical_threshold = 5.0  # seconds
        
        # Statistics
        self.stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'avg_time': 0.0,
            'min_time': float('inf'),
            'max_time': 0.0,
            'errors': 0,
            'slow_calls': 0
        })
    
    def monitor(self, name: str = None, log_slow: bool = True):
        """Decorator to monitor function performance."""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)
                
                metric_name = name or f"{func.__module__}.{func.__name__}"
                start_time = time.time()
                success = True
                error_message = None
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    success = False
                    error_message = str(e)
                    raise
                finally:
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    # Create metric
                    metric = PerformanceMetric(
                        name=metric_name,
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        success=success,
                        error_message=error_message,
                        metadata={'args_count': len(args), 'kwargs_count': len(kwargs)}
                    )
                    
                    # Record metric
                    self.record_metric(metric)
                    
                    # Log slow calls
                    if log_slow and duration > self.slow_threshold:
                        logger.warning(f"Slow call detected: {metric_name} took {duration:.2f}s")
                    
                    # Log critical calls
                    if duration > self.critical_threshold:
                        logger.error(f"Critical slow call: {metric_name} took {duration:.2f}s")
            
            return wrapper
        return decorator
    
    def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric."""
        with self.lock:
            # Add to history
            self.metrics.append(metric)
            
            # Update statistics
            stats = self.stats[metric.name]
            stats['count'] += 1
            stats['total_time'] += metric.duration
            stats['avg_time'] = stats['total_time'] / stats['count']
            stats['min_time'] = min(stats['min_time'], metric.duration)
            stats['max_time'] = max(stats['max_time'], metric.duration)
            
            if not metric.success:
                stats['errors'] += 1
            
            if metric.duration > self.slow_threshold:
                stats['slow_calls'] += 1
    
    def get_statistics(self, name: str = None) -> Dict[str, Any]:
        """Get performance statistics."""
        with self.lock:
            if name:
                return self.stats.get(name, {}).copy()
            else:
                return {k: v.copy() for k, v in self.stats.items()}
    
    def get_recent_metrics(self, minutes: int = 5) -> list:
        """Get recent metrics within specified time window."""
        cutoff_time = time.time() - (minutes * 60)
        
        with self.lock:
            recent_metrics = [
                metric for metric in self.metrics
                if metric.start_time >= cutoff_time
            ]
        
        return recent_metrics
    
    def get_slow_calls(self, threshold: float = None) -> list:
        """Get calls that exceeded the threshold."""
        if threshold is None:
            threshold = self.slow_threshold
        
        with self.lock:
            slow_calls = [
                metric for metric in self.metrics
                if metric.duration > threshold
            ]
        
        return slow_calls
    
    def get_error_calls(self) -> list:
        """Get calls that resulted in errors."""
        with self.lock:
            error_calls = [
                metric for metric in self.metrics
                if not metric.success
            ]
        
        return error_calls
    
    def clear_history(self):
        """Clear performance history."""
        with self.lock:
            self.metrics.clear()
            self.stats.clear()
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        with self.lock:
            total_calls = sum(stats['count'] for stats in self.stats.values())
            total_time = sum(stats['total_time'] for stats in self.stats.values())
            total_errors = sum(stats['errors'] for stats in self.stats.values())
            total_slow_calls = sum(stats['slow_calls'] for stats in self.stats.values())
            
            # Find top slowest functions
            slowest_functions = sorted(
                self.stats.items(),
                key=lambda x: x[1]['avg_time'],
                reverse=True
            )[:10]
            
            # Find most called functions
            most_called = sorted(
                self.stats.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:10]
            
            # Find functions with most errors
            most_errors = sorted(
                self.stats.items(),
                key=lambda x: x[1]['errors'],
                reverse=True
            )[:10]
            
            return {
                'summary': {
                    'total_calls': total_calls,
                    'total_time': total_time,
                    'average_time': total_time / total_calls if total_calls > 0 else 0,
                    'total_errors': total_errors,
                    'error_rate': total_errors / total_calls if total_calls > 0 else 0,
                    'total_slow_calls': total_slow_calls,
                    'slow_call_rate': total_slow_calls / total_calls if total_calls > 0 else 0
                },
                'slowest_functions': slowest_functions,
                'most_called_functions': most_called,
                'functions_with_most_errors': most_errors,
                'recent_metrics_count': len(self.metrics),
                'generated_at': datetime.now().isoformat()
            }
    
    def set_thresholds(self, slow_threshold: float = None, critical_threshold: float = None):
        """Set performance thresholds."""
        if slow_threshold is not None:
            self.slow_threshold = slow_threshold
        if critical_threshold is not None:
            self.critical_threshold = critical_threshold
    
    def enable(self):
        """Enable performance monitoring."""
        self.enabled = True
        logger.info("Performance monitoring enabled")
    
    def disable(self):
        """Disable performance monitoring."""
        self.enabled = False
        logger.info("Performance monitoring disabled")

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def monitor_performance(name: str = None, log_slow: bool = True):
    """Convenience decorator for performance monitoring."""
    return performance_monitor.monitor(name, log_slow)

def get_performance_report() -> Dict[str, Any]:
    """Get a performance report."""
    return performance_monitor.generate_report()

def record_custom_metric(name: str, duration: float, success: bool = True, 
                        error_message: str = None, metadata: Dict[str, Any] = None):
    """Record a custom performance metric."""
    metric = PerformanceMetric(
        name=name,
        start_time=time.time() - duration,
        end_time=time.time(),
        duration=duration,
        success=success,
        error_message=error_message,
        metadata=metadata or {}
    )
    performance_monitor.record_metric(metric)

