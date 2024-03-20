#include "point_src.h"

// Function definition
struct Point new_point(int x, int y)
{
    struct Point p = {x, y};
    return p;
}