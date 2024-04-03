from positions_compiled_c import calc_positions

if __name__ == "__main__":
    result = calc_positions("|1|2 0|1|32000000".encode(), 32000000, 1)
    print(result)
