"""
Pipeline Coordinator Package.
Orchestrates end-to-end execution of data loaders, models, and visualizers.
"""

from .coordinator import run_full_pipeline_workflow

__all__ = ["run_full_pipeline_workflow"]
