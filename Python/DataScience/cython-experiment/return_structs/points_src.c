#include "points_src.h"
#include <stdlib.h>

// Create a set of n points.
Points create(int start_x, int start_y, int offset_x, int offset_y, int n)
{
    // Setup a Points struct as the result
    Points ps;
    ps.n = n;

    // Allocate memory for the n points
    ps.arr = (Point *)malloc(n * sizeof(Point));
    if (ps.arr == NULL)
    {
        exit(-1);
    }

    // Make each of the n points
    for (int i = 0; i < n; i++)
    {
        if (i == 0)
        {
            ps.arr[i].x = start_x;
            ps.arr[i].y = start_y;
        }
        else
        {
            ps.arr[i].x = ps.arr[i - 1].x + offset_x;
            ps.arr[i].y = ps.arr[i - 1].y + offset_y;
        }
    }

    return ps;
}