// Type alias
type MyValue = string | number;

function getValue(): MyValue {
    return "abc";
}

const value1: MyValue = getValue();

function printString(x: string) {
    console.log(x);
}

// printString(value1);
// Argument of type 'MyValue' is not assignable to parameter of type 'string'.
//  Type 'number' is not assignable to type 'string'.ts(2345)

printString(value1 as string);