// -----------------------------------------------------------------------------
// Function type expression
// -----------------------------------------------------------------------------

type Greeter = (name: string) => void;

function greeter(fn: Greeter) {
    fn("Hello, Chris");
}

function printToConsole(s: string): void {
    console.log(s);
}

greeter(printToConsole);

// -----------------------------------------------------------------------------
// Call signature
// -----------------------------------------------------------------------------

type DescribableFunction = {
    description: string; // Property
    (arg: number): boolean;  // Function
};

function runFunction(fn: DescribableFunction, value: number) {
    console.log(`'${fn.description}' returned ${fn(value)} for ${value}`);
}

function func1(arg: number): boolean {
    return arg % 2 == 0;
}
func1.description = "is even";

runFunction(func1, 9);
