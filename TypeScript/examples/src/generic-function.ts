// -----------------------------------------------------------------------------
// Generic function
// -----------------------------------------------------------------------------

function mapAndFilter<T>(values: T[], fn: (value: T) => T | null): T[] {
    return values.map(fn).filter(v => v !== null);
}

function mapper(value: number): number | null {
    return (value<10) ? value*2 : null;
}

const result = mapAndFilter([1,5,10,15], mapper);
console.log(result);

// -----------------------------------------------------------------------------
// Constraints
// -----------------------------------------------------------------------------

function longest<T extends {length: number}>(a: T, b: T): T {
    return (a.length > b.length) ? a : b;
}

console.log(longest([1,2], [1,2,3]));