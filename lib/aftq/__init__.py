# AFT-Q Package
"""
AFT-Q: Quantum-Native Compression Interface

Provides coherence analysis for quantum-suitable compression.
Full implementation available in cr8OS Commercial SDK.

Usage:
    from lib.aftq.core import AFTQCompressor
    
    compressor = AFTQCompressor()
    seed = compressor.compress(data)
    print(seed.summary())
"""

from .core import (
    AFTQCompressor,
    AFTQDecompressor,
    QuantumSeed,
    CoherenceClassifier,
)

__version__ = "Q.1.0.0"
__author__ = "cr8OS Foundation / Aevov Research"
