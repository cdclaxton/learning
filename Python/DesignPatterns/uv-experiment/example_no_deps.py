import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Hello, World!")
    else:
        print(f"Hello, {sys.argv[1]}")
