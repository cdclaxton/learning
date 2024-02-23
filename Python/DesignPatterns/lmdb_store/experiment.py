import lmdb
import os
import pickle
import shutil

if __name__ == "__main__":

    folder = "./db"
    if os.path.exists(folder):
        print(f"Removing folder: {folder}")
        shutil.rmtree(folder)

    env = lmdb.open(folder, map_size=100000)

    # Data to write
    data = {
        "t0": ["e-0"],
        "t1": ["e-0", "e-1", "e-2"],
        "t2": ["e-3", "e-5"]
    }

    # Write some data
    with env.begin(write=True) as txn:
        for key, values in data.items():
            # Pickle the list
            picked_values = pickle.dumps(values)

            # Store
            print(f"Storing key: {key}, values: {values}")
            txn.put(key.encode("ascii"), picked_values)
        
    # Read the data
    with env.begin() as txn:
        for key in data:
            raw = txn.get(key.encode("ascii"))
            unpickled_values = pickle.loads(raw)
            assert unpickled_values == data[key]
            print(f"Key: {key}, values: {unpickled_values}")

        # Get the data for a key that doesn't exist
        raw = txn.get("token".encode("ascii"))
        assert raw is None

    print(env.stat())

    # Clean up
    shutil.rmtree(folder)
