#include <assert.h>

void func1(int *a)
{
    *a = 100;
}

int main(void)
{
    // Constant value
    const int a = 10;
    // a = 20;  error: assignment of read-only variable ‘a’
    assert(a == 10);

    // Pointer to a constant -- can't change the value the pointer points to,
    // but the pointer itself can be changed
    int b = 20;
    int c = 40;
    const int *ptr = &b;
    // *ptr = 30; error: assignment of read-only location ‘*ptr’
    ptr = &c;
    assert(*ptr == 40);

    // Const pointer -- can't change the pointer, but can change the value it
    // points to
    int d = 100;
    int *const ptr2 = &d;
    *ptr2 = 30;
    assert(d == 30);
    // ptr2 = &b;  error: assignment of read-only variable ‘ptr2’

    // Can't change the pointer or the value it points to
    int e = 200;
    const int *const ptr3 = &e;
    assert(*ptr3 == 200);
    // *ptr3 = 300;  error: assignment of read-only location ‘*(const int *)ptr3’
    // ptr3 = &d;  error: assignment of read-only variable ‘ptr3’

    // Pass a pointer to a function func1()
    int f = 15;
    func1(&f);
    assert(f == 100);

    return 0;
}