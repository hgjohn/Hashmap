# Name: Hayden Johnston
# OSU Email: johnsth9@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/9/2023
# Description: Hashmap implementation with separate chaining


from include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Receives key and value to insert into hash map
        """

        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # get hash and index
        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]

        # check if bucket contains key to update value
        key_exists =  bucket.contains(key)
        if key_exists is not None:
            key_exists.value = value
            return None

        # else key does not exist and is added
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Return Number of empty buckets in the hash map
        """

        # count buckets with length 0
        bucket_count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                bucket_count += 1
        return bucket_count

    def table_load(self) -> float:
        """
        Return the current load factor of the hash map
        """

        load_factor = self._size / self._capacity
        return load_factor

    def clear(self) -> None:
        """
        Clear the hash table without changing capacity
        """

        new_map = HashMap(self._capacity, self._hash_function)
        self._buckets = new_map._buckets
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the table to new_capacity
        All hashtable links are rehashed
        """

        if new_capacity < 1:
            return None
        
        # capacity must be prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # initialize new map and reset capacity to 1 or 2 if necessary
        new_map = HashMap(new_capacity, self._hash_function)
        if new_capacity == 1 or new_capacity == 2:
            new_map._capacity = new_capacity
            new_map._buckets.pop()
            if new_capacity == 1:
                new_map._buckets.pop()
        
        # rehash every key into new table
        for i in range(self._capacity):
            if self._buckets[i] is not None:
                for j in self._buckets[i]:
                    new_map.put(j.key, j.value)
        
        self._buckets = new_map._buckets
        self._capacity = new_map._capacity
        
    def get(self, key: str) -> object:
        """
        Receives key to search hash map
        Return value associated with key or None
        """
        
        # search hashed bucket for key and return value
        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]
        node = bucket.contains(key)
        if node is not None:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Receives key to search for in hashamp
        Returns True if key exists in data structure
        """
        
        # search hashed bucket for key and return True if exists
        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]
        if bucket.contains(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Receives key to remove its value from hash map
        """
        
        # search hashed bucket for key and delete node if exists
        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]
        node = bucket.contains(key)
        if node is not None:
            bucket.remove(node.key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array containing tuples of key/value pairs
        """

        # iterate through each bucket to build arr of kv pairs
        kv_array = DynamicArray()
        for i in range(self._capacity):
            bucket = self._buckets[i]
            for node in bucket:
                if node is not None:
                    kv_array.append((node.key, node.value))
        return kv_array

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Return a tuple that contains:
    a dynamic array containing mode values and
    an integer representing the mode frequency
    """

    map = HashMap()
    
    # add key from da with value = frequency
    for i in range(da.length()):
        if map.get(da[i]) is not None:
            map.put(da[i], map.get(da[i]) + 1)
        else:
            map.put(da[i], 1)
    sorted_da = map.get_keys_and_values()

    # get max frequency and build mode array
    mode = DynamicArray()
    max = 0
    for i in range(sorted_da.length()):
        frequency = sorted_da[i][1]
        if frequency > max:
            max = frequency
            mode = DynamicArray()
            mode.append(sorted_da[i][0])
        elif frequency == max:
            mode.append(sorted_da[i][0])

    return (mode, max)
