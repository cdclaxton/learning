import math
import matplotlib.pyplot as plt

def num_cells(width: int, cell_width, gap_width: int) -> int:
    return math.floor((width - gap_width)/(cell_width+gap_width))

def calc_left_gap(width: int, n_cells: int, cell_width: int, gap_width: int) -> int:
    return math.floor((width - n_cells*(cell_width + gap_width) + gap_width) / 2)

if __name__ == "__main__":
    width = 480
    height = 360

    cell_width = 80
    cell_height = 30
    gap = 10

    # Calculate the number of cells horizontally and vertically
    n_cells_horizontally = num_cells(width, cell_width, gap)
    print(f"Number of cells horizontally = {n_cells_horizontally}")

    n_cells_vertically = num_cells(height, cell_height, gap)
    print(f"Number of cells vertically = {n_cells_vertically}")

    # Calculate the left gap
    gap_left = calc_left_gap(width, n_cells_horizontally, cell_width, gap)

    # Calculate the top gap
    gap_top = calc_left_gap(height, n_cells_vertically, cell_height, gap)

    # Draw the grid
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    ax.add_patch(plt.Rectangle((0,0), width, height, fill=True))
    ax.set_xlim([-10, width+10])
    ax.set_ylim([-10, height+10])

    for i in range(n_cells_vertically):
        for j in range(n_cells_horizontally):

            x = gap_left + j*(cell_width + gap)
            y = gap_top + i*(cell_height + gap)

            ax.add_patch(plt.Rectangle((x,y), cell_width, cell_height, fill=False))

    plt.show()
