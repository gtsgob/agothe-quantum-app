"""
Output formatting utilities
"""

from typing import Dict, Any

def format_analysis_report(analysis: Dict[str, Any], title: str = "Analysis Report") -> str:
    """
    Format analysis results as readable text report

    Args:
        analysis: Analysis dictionary
        title: Report title

    Returns:
        Formatted string report
    """
    lines = []
    lines.append("=" * 60)
    lines.append(title.center(60))
    lines.append("=" * 60)

    def format_dict(d: Dict, indent: int = 0):
        """Recursively format dictionary"""
        for key, value in d.items():
            prefix = "  " * indent
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                format_dict(value, indent + 1)
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    lines.append(f"{prefix}  - {item}")
            else:
                lines.append(f"{prefix}{key}: {value}")

    format_dict(analysis)
    lines.append("=" * 60)

    return "\n".join(lines)

def format_metric(value: float, precision: int = 3) -> str:
    """
    Format a metric value with consistent precision

    Args:
        value: Metric value
        precision: Number of decimal places

    Returns:
        Formatted string
    """
    return f"{value:.{precision}f}"

def format_percentage(value: float, precision: int = 1) -> str:
    """
    Format a value as percentage

    Args:
        value: Value (0.0-1.0 or already as percentage)
        precision: Number of decimal places

    Returns:
        Formatted percentage string
    """
    if value <= 1.0:
        value *= 100
    return f"{value:.{precision}f}%"
