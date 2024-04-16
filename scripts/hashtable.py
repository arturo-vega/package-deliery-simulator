# Source: WGU code repository W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
# Creates a hashtable and uses the python hashing function to hash the key
# The key is the ID of the package
class HashTable:
    def __init__(self, size):
        self.size = size
        self.slots = [[] for _ in range(size)]

    def insert(self, key, package):
        bucket = hash(key) % len(self.slots)
        bucket_list = self.slots[bucket]

        for i in bucket_list:
            if i[0] == key:
                i[1] = package
                return True

        key_value = [key, package]
        bucket_list.append(key_value)
        return True

    def get(self, key):
    # Get the hash index
        bucket = hash(key) % len(self.slots)
        bucket_list = self.slots[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]

        return None # No pair matches key