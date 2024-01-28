import logging
import sys

WEIGHT_OFFSET = sys.getsizeof(bytearray())
KB2B = 1000

logger = logging.getLogger('waster')


class MemoryWaster:
    """
    The core of the memory waster, it managed the precise amount of memory that is consummed.

    The waster has a target that can be edited by calling the methods. Once target is what is wanted, a call to refresh
    will update the internal memory consumption to the wanted target. The cycle is always:

    #. Edit the target as many times as needed
    #. Refresh the waster
    """

    def __init__(self, initial_amount_kb: int):
        self._target_kb = initial_amount_kb
        self._weight = bytearray()
        logger.debug(f'initialized with a target of {initial_amount_kb} kB')

    @property
    def target_kb(self) -> int:
        """
        Get the wasted amount in kB, this value does always represent the actual wasted memory. When modified,
        call the refresh method to update the internal wasted memory.

        :return: kilobytes
        :rtype: int
        """
        return self._target_kb

    @property
    def current_kb(self) -> int:
        """
        Get the actual wasted amount of memory.

        :return: kilobytes
        :rtype: int
        """
        return int((sys.getsizeof(self._weight) - WEIGHT_OFFSET) / KB2B)

    @property
    def need_refresh(self) -> bool:
        """
        Check if the waster target and current values are out of sync and needs to be refreshed.

        :rtype: bool
        """
        return self._target_kb != self.current_kb

    def set(self, value_kb: int):
        """
        Set the current value regardless of what it was before. Refresh must be called after.

        :param value_kb: the new target in kilobyte
        """
        if value_kb < 0:
            raise ValueError(f'Target value must be greater or equal than 0, got {value_kb}')

        self._target_kb = value_kb
        logger.debug(f'memory target set to {value_kb} kB')

    def decrease(self, amount_kb: int):
        """
        Decrease the current target with a bound on 0 (keeps the target <= 0). Refresh must be called after.

        :param amount_kb: the mount to remove from the current target
        """
        if amount_kb < 0:
            raise ValueError(f'Amount must be greater or equal than 0, got {amount_kb}')

        if amount_kb >= self._target_kb:
            self._target_kb = 0
        else:
            self._target_kb -= amount_kb

        logger.debug(f'memory target decreased by {amount_kb} kB to {self._target_kb}')

    def increase(self, amount_kb: int):
        """
        Increase the current target. Refresh must be called after.

        :param amount_kb: the mount to add to the current target
        """
        if amount_kb < 0:
            raise ValueError(f'Amount must be greater or equal than 0, got {amount_kb}')

        self._target_kb += amount_kb
        logger.debug(f'memory target increased by {amount_kb} kB to {self._target_kb}')

    def clear(self):
        """
        Reset the target consumption to 0. Refresh must be called after.
        """
        self._target_kb = 0
        logger.debug(f'memory target reset to 0')

    def refresh(self):
        """
        Refresh the internal waster so its memory consumption matches the target.
        """
        self._weight = bytearray(self._target_kb * KB2B)
        logger.debug(f'memory consumption refreshed target={self._target_kb}kB, consumed={self.current_kb}')


def create_memory_waster(initial_wasted_amount_kb: int = 0) -> MemoryWaster:
    """
    Initialize a memory waster with a value but does not refresh it so the memory is not consumed yet.

    :param initial_wasted_amount_kb: amount of initial memory to waste in kilobyte
    :return: the memory waster
    :rtype: MemoryWaster
    """
    return MemoryWaster(initial_wasted_amount_kb)
