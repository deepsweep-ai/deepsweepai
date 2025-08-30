"""
DeepSweep AI: AI Agent Security Scanner
"""

from deepsweepai.scanner import Scanner, TestResult
from deepsweepai.adversarial import AdversarialEngine
from deepsweepai.compliance import ComplianceMapper

__version__ = "0.2.0"  # Bump version for new features
__author__ = "Brad McEvilly"
__email__ = "brad@deepsweep.ai"

__all__ = ["Scanner", "TestResult", "AdversarialEngine", "ComplianceMapper"]