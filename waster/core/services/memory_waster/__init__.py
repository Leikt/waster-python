"""
Service that manage the wasting of the memory. This allows the system to consume a specific amount of memory.
"""
from ._waster import MemoryWaster, create_memory_waster

__all__ = ['MemoryWaster', 'create_memory_waster']
