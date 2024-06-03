// Template literals are strings with embedded expressions (can be variables and 
// function calls)
const name = "Chris";
console.log(`Hello ${name}`);  // Hello Chris

// Single and double quotes can occur inside template literals
const token = "address";
console.log(`Token is '${token}'`);  // Token is 'address'

// Expressions are evaluated when the template literals are evaluated
let value = 4;
const msg1 = `The value is ${value}`;
const msg2 = () => `The value is ${value}`;
value = 0;
console.log(`msg1: ${msg1}`);  // msg1: The value is 4
console.log(`msg2(): ${msg2()}`);  // msg2(): The value is 0

// Function calls can occur inside template literals
const firstName = "Sam";
const lastName = "Taylor";
console.log(`${lastName.toUpperCase()}, ${firstName}`);  // TAYLOR, Sam

// Template literal tagged with String.raw
console.log(String.raw`Some special characters \ \n \b`);
