#!/usr/bin/env python3
"""Least Frequently Used caching module.
"""
from collections import defaultdict, OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Represents an object that allows storing and
    retrieving items from a dictionary with an LFU
    removal mechanism when the limit is reached.
    """
    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.cache_data = {}
        self.freq_map = defaultdict(int)  # To track frequency of each key
        self.lru_order = OrderedDict()     # To track order of usage for LRU

    def put(self, key: str, item: any) -> None:
        """Adds an item in the cache.
        
        Args:
            key (str): The key to store the item under.
            item (any): The item to store.
        """
        if key is None or item is None:
            return

        # Add or update the item
        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq_map[key] += 1  # Increment frequency
            self.lru_order.move_to_end(key)  # Update LRU order
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used items
                min_freq = min(self.freq_map.values())
                lfu_candidates = [k for k, v in self.freq_map.items() if v == min_freq]

                # If there are multiple LFU candidates, use LRU to determine which to discard
                lfu_key = lfu_candidates[0]  # Start with the first candidate
                if len(lfu_candidates) > 1:
                    lfu_key = min(lfu_candidates, key=lambda k: self.lru_order[k])

                # Discard the LFU item
                print("DISCARD:", lfu_key)
                del self.cache_data[lfu_key]
                del self.freq_map[lfu_key]
                del self.lru_order[lfu_key]

            # Add the new item
            self.cache_data[key] = item
            self.freq_map[key] = 1  # Frequency starts at 1
            self.lru_order[key] = None  # Add to LRU order (value is irrelevant)
        
        self.lru_order.move_to_end(key)  # Update LRU order

    def get(self, key: str) -> any:
        """Retrieves an item by key.
        
        Args:
            key (str): The key of the item to retrieve.
        
        Returns:
            any: The item associated with the key, or None if not found.
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and LRU order
        self.freq_map[key] += 1
        self.lru_order.move_to_end(key)

        return self.cache_data[key]
