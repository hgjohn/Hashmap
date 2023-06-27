## Hash Map 
Hash map implementation in Python 3 based on the Python dictionary model.  Includes two methods for collision resolution: Separate Chaining and Open Addressing with quadratic probing.
Insert, get, and remove functions are all constant time complexity due to the nature of hashing each key to its preferred index. 

# Separate Chaining
This method of collision resolution uses a Dynamic Array where each index represents a bucket.  Each bucket is represented as a linked list.  To add a value, the key is hashed to its index and added to the linked list.  In this implementation, values are only added to the front of each linked list in order to reduce run time.  The table load in separate chaining can exceed 1, since each bucket can contain multiple values.
![Screenshot 2023-06-27 at 12-40-59 Exploration Hash Table Collisions DATA STRUCTURES (CS_261_406_S2023)](https://github.com/hgjohn/Hashmap/assets/103093070/438fe75a-0a2f-4d14-acf8-453558c3d759)
Example: Separate chaining implementation.

# Open Addressing  
This method of collision resolution uses a Dynamic Array alone.  If the hashed index for a value is occupied, the next index is probed (quadratically in this implementation).  If the array is Upon removal, a value is replaced by a Tombstone value (__TS__) so that the index may be filled by a new value.  The table load in open addressing can not exceed 1, since a table of n capacity can only hold n values.
![Screenshot 2023-06-27 at 12-41-04 Exploration Hash Table Collisions DATA STRUCTURES (CS_261_406_S2023)](https://github.com/hgjohn/Hashmap/assets/103093070/8b246133-e2ce-41be-8989-2683cde96381)
Example: Open Addressing implementation with linear probing. 
