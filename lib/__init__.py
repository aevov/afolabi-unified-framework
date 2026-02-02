# AFT Library - __init__.py
"""
Afolabi Field Theory Compression Library
========================================

This package provides the compression engines for the Afolabi Unified Framework:

- aft2: AFT 2.0 with 333,333:1 compression (3,333 glyph dictionary)
- aft3: AFT 3.0 with 10⁹:1 compression (hierarchical recursion)
- aftq: AFT-Q with ∞:1 compression (quantum-native, theoretical)

Usage:
    from lib.aft2.core import AFT2Compressor
    from lib.aft3.core import AFT3Compressor
    
    # AFT 2.0
    compressor = AFT2Compressor()
    seed = compressor.compress(data)
    
    # AFT 3.0 (hierarchical)
    compressor = AFT3Compressor()
    hseed = compressor.compress(data)
    print(hseed.summary())
"""

__version__ = "2.0.0-alpha"
__author__ = "cr8OS Foundation / Aevov Research"
