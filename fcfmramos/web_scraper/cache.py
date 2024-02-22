import pickle  # nosec B403
import os

from typing import Set
from hashlib import md5

from fcfmramos.web_scraper.config import CACHE_DIR


class HashCache:
    """For caching hashes of values to check if they have been seen before."""

    def __init__(self, file_name: str) -> None:
        self._path = CACHE_DIR / file_name
        self._cache = self._load()

    def add(self, value: str) -> None:
        """Adds the hash of the value to the cache.

        Args:
            value (str): The value to hash and add to the cache.
        """
        self._cache.add(self._hash(value))

    def has(self, value: str) -> bool:
        """Checks if the hash of the value is in the cache.

        Args:
            value (str): The value to hash and check if it is in the cache.

        Returns:
            bool: True if the hash of the value is in the cache.
        """
        return self._hash(value) in self._cache

    def save(self) -> None:
        """Saves the cache to disk."""
        with open(self._path, "wb") as file:
            pickle.dump(self._cache, file)

    def _load(self) -> Set[str]:
        """Loads the cache from disk if it exists.

        Returns:
            Set[str]: Empty set or loaded cache.
        """
        if not os.path.exists(self._path):
            return set()

        with open(self._path, "rb") as file:
            return pickle.load(file)  # nosec B301

    def _hash(self, value: str) -> str:
        """Hashes the value.

        Args:
            value (str): The value to hash.

        Returns:
            str: The hash of the value.
        """
        return md5(value.encode()).hexdigest()
