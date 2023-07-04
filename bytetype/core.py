# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['KILOBYTE', 'bytes_idx', 'bytes_to_size', 'BytesUnit', 'Bytes']

# %% ../nbs/00_core.ipynb 3
import os, math
from dataclasses import KW_ONLY, dataclass, field
from enum import StrEnum
from typing import Union, List, Optional

# %% ../nbs/00_core.ipynb 4
KILOBYTE = 1024

# %% ../nbs/00_core.ipynb 5
def bytes_idx(bytes:float) -> int:
    """Calculate the index of the byte unit for a byte count.

    Parameters
    ----------
    bytes : float
        The byte count.

    Returns
    -------
    int
        The index of the byte unit.
    """
    idx = int(math.floor(math.log(bytes, KILOBYTE)))
    return idx

def bytes_to_size(bytes:float, decimals: Optional[int] = 2) -> float:
    """Calculate the size in appropriate byte unit for a byte count.

    Parameters
    ----------
    bytes : float
        The byte count.
    decimals : int, optional
        The number of decimal places to round to (default is 2).

    Returns
    -------
    float
        The size in the appropriate byte unit.
    """
    idx = bytes_idx(bytes)
    power = math.pow(KILOBYTE, idx)
    size = round(bytes / power, decimals)
    return size

# %% ../nbs/00_core.ipynb 6
class BytesUnit(StrEnum):
    """An enumeration of byte units.
    
    This class defines a string enumeration representing various byte units.
    It provides methods for calculating size and determining appropriate unit from a byte count.
    """
    B = 'B'
    KB = 'KB'
    MB = 'MB'
    GB = 'GB'
    TB = 'TB'
    PB = 'PB'
    EB = 'EB'
    ZB = 'ZB'
    YB = 'YB'

    @staticmethod
    def calc_idx(bytes:float) -> int:
        """Calculate the index of the byte unit for a byte count.
        
        Parameters
        ----------
        bytes : float
            The byte count.

        Returns
        -------
        int
            The index of the byte unit.
        """
        return bytes_idx(bytes)
    
    @staticmethod
    def calc_size(bytes:float, decimals: Optional[int] = 2) -> float:
        """Calculate the size in appropriate byte unit for a byte count.
        
        Parameters
        ----------
        bytes : float
            The byte count.
        decimals : int, optional
            The number of decimal places to round to (default is 2).

        Returns
        -------
        float
            The size in the appropriate byte unit.
        """
        return bytes_to_size(bytes, decimals)

    @classmethod
    def unit(cls, bytes:float) -> str:
        """Determine the appropriate byte unit for a byte count.
        
        Parameters
        ----------
        bytes : float
            The byte count.

        Returns
        -------
        str
            The appropriate byte unit.
        """
        idx = cls.calc_idx(bytes)
        key = cls.keys()[idx]    
        return key
    
    @classmethod
    def keys(cls) -> List[str]:
        """Get the keys of the enumeration.

        Returns
        -------
        List[str]
            The keys of the enumeration.
        """
        return list(cls._member_map_.keys())
    
    @classmethod
    def from_bytes(cls, bytes:float) -> 'BytesUnit':
        """Create a BytesUnit instance from a byte count.
        
        Parameters
        ----------
        bytes : float
            The byte count.

        Returns
        -------
        BytesUnit
            The BytesUnit instance representing the appropriate byte unit.
        """
        unit = cls.unit(bytes)
        return cls(unit)

# %% ../nbs/00_core.ipynb 7
@dataclass
class Bytes:
    """A class for representing sizes in various byte units."""
    bytes: int = field(default=0, repr=False,)
    round: Optional[int] = field(default=2, repr=False)
    
    unit: BytesUnit = field(default=BytesUnit.B, init=False)
    size: float = field(default=0.0, init=False)

    def __post_init__(self):
        self.unit = BytesUnit.from_bytes(self.bytes)
        self.size = BytesUnit.calc_size(self.bytes, self.round)

    def __repr__(self) -> str:
        return f'{self.size} {self.unit}'
    
    def __add__(self, other: Union['Bytes', int]):
        """Add two Bytes instances or a Bytes instance and a byte count.
        
        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        Bytes
            The Bytes instance representing the total size.
        """
        if isinstance(other, Bytes):
            total_bytes = self.bytes + other.bytes
        else:
            total_bytes = self.bytes + other
        return Bytes(total_bytes, round=self.round)

    def __sub__(self, other: Union['Bytes', int]):
        """Subtract a Bytes instance or a byte count from this Bytes instance.
        
        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        Bytes
            The Bytes instance representing the remaining size.
        """
        if isinstance(other, Bytes):
            total_bytes = self.bytes - other.bytes
        else:
            total_bytes = self.bytes - other
        if total_bytes < 0: total_bytes = 0
        return Bytes(total_bytes, round=self.round)
    
    def __mul__(self, other: Union['Bytes', int]):
        """Multiply this Bytes instance by a Bytes instance or a byte count.
        
        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        Bytes
            The Bytes instance representing the total size.
        """
        if isinstance(other, Bytes):
            total_bytes = self.bytes * other.bytes
        else:
            total_bytes = self.bytes * other
        return Bytes(total_bytes, round=self.round)

    def __truediv__(self, other: Union['Bytes', int]):
        """Divide this Bytes instance by a Bytes instance or a byte count.
        
        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        Bytes
            The Bytes instance representing the total size.
        """
        if isinstance(other, Bytes):
            total_bytes = self.bytes / other.bytes
        else:
            total_bytes = self.bytes / other
        return Bytes(total_bytes, round=self.decimals)

    @staticmethod
    def from_file(file_path: str, round: Optional[int] = 2) -> 'Bytes':
        """Create a Bytes instance representing the size of a file.
        
        Parameters
        ----------
        file_path : str
            The path to the file.
        decimals : int, optional
            The number of decimal places to round to (default is 2).

        Returns
        -------
        Bytes
            The Bytes instance representing the size of the file.
        """
        size = os.path.getsize(file_path)
        return Bytes(size, round=round)

    @staticmethod
    def from_dir(dir_path: str, round: Optional[int] = 2) -> 'Bytes':
        """Create a Bytes instance representing the total size of a directory.
        
        Parameters
        ----------
        dir_path : str
            The path to the directory.
        decimals : int, optional
            The number of decimal places to round to (default is 2).

        Returns
        -------
        Bytes
            The Bytes instance representing the total size of the directory.
        """
        total = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)
        return Bytes(total, round=round)
    
    def to_bytes(self) -> int:
        """Convert the Bytes instance to a byte count.

        Returns
        -------
        int
            The byte count.
        """
        return self.bytes
    

    def __lt__(self, other: Union['Bytes', int]) -> bool:
        """Less than comparison between two Bytes instances or a Bytes instance and a byte count.

        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        bool
            True if this Bytes instance is less than the other, False otherwise.
        """
        if isinstance(other, Bytes):
            return self.bytes < other.bytes
        else:
            return self.bytes < other

    def __le__(self, other: Union['Bytes', int]) -> bool:
        """Less than or equal to comparison between two Bytes instances or a Bytes instance and a byte count.

        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        bool
            True if this Bytes instance is less than or equal to the other, False otherwise.
        """
        if isinstance(other, Bytes):
            return self.bytes <= other.bytes
        else:
            return self.bytes <= other

    def __gt__(self, other: Union['Bytes', int]) -> bool:
        """Greater than comparison between two Bytes instances or a Bytes instance and a byte count.

        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        bool
            True if this Bytes instance is greater than the other, False otherwise.
        """
        if isinstance(other, Bytes):
            return self.bytes > other.bytes
        else:
            return self.bytes > other

    def __ge__(self, other: Union['Bytes', int]) -> bool:
        """Greater than or equal to comparison between two Bytes instances or a Bytes instance and a byte count.

        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        bool
            True if this Bytes instance is greater than or equal to the other, False otherwise.
        """
        if isinstance(other, Bytes):
            return self.bytes >= other.bytes
        else:
            return self.bytes >= other

    def __eq__(self, other: Union['Bytes', int]) -> bool:
        """Equality comparison between two Bytes instances or a Bytes instance and a byte count.

        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        bool
            True if this Bytes instance is equal to the other, False otherwise.
        """
        if isinstance(other, Bytes):
            return self.bytes == other.bytes
        else:
            return self.bytes == other

    def __ne__(self, other: Union['Bytes', int]) -> bool:
        """Not equal to comparison between two Bytes instances or a Bytes instance and a byte count.

        Parameters
        ----------
        other : Bytes or int
            The other Bytes instance or byte count.

        Returns
        -------
        bool
            True if this Bytes instance is not equal to the other, False otherwise.
        """
        if isinstance(other, Bytes):
            return self.bytes != other.bytes
        else:
            return self.bytes != other
