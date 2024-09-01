#!/usr/bin/python3
""" BaseCaching module
"""
from collections import OrderedDict
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """A caching system that inherits from BaseCaching and does not have a
    limit on the number of items it can store.
    """
    def __init__(self):
        """Initializes the cache and calls the parent class's init method.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Assigns the item value to the key in the dictionary self.cache_data.
        If key or item is None, this method should not do anything.
        If the number of items in self.cache_data is higher that BaseCaching.MAX_ITEMS:
           must discard the first item put in cache (FIFO algorithm)
           must print DISCARD: with the key discarded and following by a new line

        Args:
            key (any): param1.
            item (any): param2.
        """
        if key is None or item is None:
            return
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            print("Discared: {}".format(first_key))
        self.cache_data[key] = item

    def get(self, key):
        """Returns the value in self.cache_data linked to key.
        If key is None or if the key doesn't exist in self.cache_data,
        return None.

        Args:
            key (any): param1.
        """
        return self.cache_data.get(key, None)
