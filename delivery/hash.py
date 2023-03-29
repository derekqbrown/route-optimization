# Creates a hash map   space-complexity = O(n)
class HashMap:

    # Initializes the hash map   time-complexity = O(1)
    def __init__(self):
        self.hash_map = [[] for _ in range(10)]

    # Inserts a package into hash map   time-complexity = O(n)
    def insert(self, key, val):
        # The hash key used for insertion
        hash_key = key % len(self.hash_map)

        # The bucket where the package will be stored
        bucket = self.hash_map[hash_key]

        # If the package is already in the bucket, update the package instead of insertion
        for package in bucket:
            if package[0] == key:
                package[1] = val
                return True

        # Insert into the bucket
        bucket.append([key, val])
        return True

    # Removes a package from hash map  time-complexity = O(n)
    def delete(self, key):
        # The hash key used for lookup
        hash_key = key % len(self.hash_map)

        # The bucket where the package is stored
        bucket = self.hash_map[hash_key]

        # If the package is in the bucket, remove the package
        for package in bucket:
            if package[0] == key:
                bucket.remove([package[0], package[1]])

    # Retrieves a package from the hash map   time-complexity = O(n)
    def find(self, key):
        # The hash key used for lookup
        hash_key = key % len(self.hash_map)

        # The bucket where the package is stored
        bucket = self.hash_map[hash_key]

        # If the package is in the bucket, return the package
        for package in bucket:
            if package[0] == key:
                return package
        # If the package was not found, this message will be returned instead
        return "Package not found"
