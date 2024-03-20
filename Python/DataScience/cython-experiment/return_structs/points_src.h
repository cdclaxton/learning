typedef struct
{
    int x;
    int y;
} Point;

typedef struct
{
    int n;      // Number of points
    Point *arr; // Array of Points
} Points;

// Function prototype
Points create(int start_x, int start_y, int offset_x, int offset_y, int n);