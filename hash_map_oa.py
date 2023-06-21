# Name: Hayden Johnston
# OSU Email: johnsth9@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/9/2023
# Description: Hashmap open addressing implementation

from include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Receive key and value to insert in hash map
        Quadratic probing is used to resolve collisions
        """
        
        if self.table_load() > 0.5:
            self.resize_table(2 * self._capacity)

        # if index is empty or tombstone value then insert at hashed index
        hash = self._hash_function(key)
        index = hash % self._capacity
        j = 0
        if self._buckets[index] is None or self._buckets[index].is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        
        # if hashed index already contains key then replace the value
        elif self._buckets[index] is not None and self._buckets[index].key == key:
            self._buckets[index].key = key
            self._buckets[index].value = value
            #self._buckets[index].is_tombstone = False
            #self._buckets[index] = HashEntry(key, value)

        # quadratic probing for empty index or tombstone
        else:
            initial_index = index
            while self._buckets[index] is not None and not self._buckets[index].is_tombstone:
                j += 1
                index = (initial_index + j ** 2) % self._capacity
                
                # break loop if matching key, check tombstone to manage _size
                if self._buckets[index] is not None and self._buckets[index].key == key:
                    if not self._buckets[index].is_tombstone:
                        self._size -= 1
                    break

            self._buckets[index] = HashEntry(key, value)
            self._size += 1

    def table_load(self) -> float:
        """
        Return current table load
        """
        
        load = self._size / self._capacity
        return load

    def empty_buckets(self) -> int:
        """
        Return current number of empty buckets
        """
        
        empty_count = self._capacity - self._size
        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Receives new_capacity to resize table
        Rehash every Hashentry into new map
        """
        
        # if new_capacity is less than current size then do nothing
        if new_capacity < self._size:
            return None
        
        # capacity must be prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # rehash every entry into new map
        new_map = HashMap(new_capacity, self._hash_function)
        for i in range(self._capacity):
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                new_map.put(self._buckets[i].key, self._buckets[i].value)

        self._buckets = new_map._buckets
        self._capacity = new_map._capacity
        
    def get(self, key: str) -> object:
        """
        Receives key to search table
        Returns value associated with key or None
        """
        
        # check for key and probe quadratically if needed
        hash = self._hash_function(key)
        index = hash % self._capacity
        j = 0
        initial_index = index
        get_value = None
        while self._buckets[index] is not None and self._buckets[index].key != key:
            j += 1
            index = (initial_index + j ** 2) % self._capacity
            
            # if key is not probed then return None
            if index == initial_index:
                return get_value

        if self._buckets[index] is not None and not self._buckets[index].is_tombstone:    
            get_value =  self._buckets[index].value

        return get_value
        
    def contains_key(self, key: str) -> bool:
        """
        Receives key to search map
        Returns True if key exists in data structure
        """
        
        if self.get(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Receives key to remove from map
        """
        
        # check for key and probe quadratically if needed
        hash = self._hash_function(key)
        index = hash % self._capacity
        j = 0
        initial_index = index
        delete_key = None
        while self._buckets[index] is not None and self._buckets[index].key != key:
            j += 1
            index = (initial_index + j ** 2) % self._capacity
            
            # if key is not probed then return None
            if index == initial_index:
                return delete_key

        if self._buckets[index] is not None and not self._buckets[index].is_tombstone:    
            delete_key =  self._buckets[index]

        if delete_key is not None:
            delete_key.is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """
        Clear hash table without changing capacity
        """
        
        new_map = HashMap(self._capacity, self._hash_function)
        self._buckets = new_map._buckets
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return all existing key/value pairs in hash map
        """
        
        contents = DynamicArray()
        for kv_pair in self:
            contents.append((kv_pair.key, kv_pair.value))
        return contents

    def __iter__(self):
        """
        Iterator method for hash table
        """
        
        self._index = 0
        return self

    def __next__(self):
        """
        Get next value and advance iterator
        """

        try:
            value = None
            while value is None or value.is_tombstone:
                value = self._buckets[self._index]
                self._index += 1
        except DynamicArrayException:
            raise StopIteration

        return value
