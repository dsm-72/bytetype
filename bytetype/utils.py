# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_utils.ipynb.

# %% auto 0
__all__ = ['bytes_idx', 'bytes_to_size']

# %% ../nbs/01_utils.ipynb 4
import os, math
from dataclasses import KW_ONLY, dataclass, field
from enum import Enum, StrEnum, IntEnum
from typing import Union, List, Optional

# %% ../nbs/01_utils.ipynb 6
from bytetype.units import (
    BYTE, KILOBYTE, MEGABYTE, GIGABYTE, TERABYTE,
    PETABYTE, EXABYTE, ZETTABYTE, YOTTABYTE
)

# %% ../nbs/01_utils.ipynb 8
def bytes_idx(nbytes: float) -> int:
    """Calculate the index of the byte unit for a byte count.

    Parameters
    ----------
    nbytes : float
        The byte count.

    Returns
    -------
    int
        The index of the byte unit.
    """
    idx = int(math.floor(math.log(nbytes, KILOBYTE)))
    return idx

# %% ../nbs/01_utils.ipynb 9
def bytes_to_size(nbytes: float, decimals: Optional[int] = 2) -> float:
    """Calculate the size in appropriate byte unit for a byte count.

    Parameters
    ----------
    nbytes : float
        The byte count.
    decimals : int, optional
        The number of decimal places to round to (default is 2).

    Returns
    -------
    float
        The size in the appropriate byte unit.
    """
    idx = bytes_idx(nbytes)
    power = math.pow(KILOBYTE, idx)
    size = round(nbytes / power, decimals)
    return size
