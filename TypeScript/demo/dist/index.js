"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
console.log("Hello TypeScript!");
// Declare an object literal with a given 'shape'
let a = {
    b: 'x',
    20: true,
    30: false,
    d: 21,
};
// Class
class Person {
    constructor(firstName, // equivalent to this.firstName = firstName
    lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }
}
const c = new Person("Bob", "Smith");
// Arrays
function buildArray() {
    let a = []; // type: any[]
    a.push(1);
    a.push(true);
    return a;
}
let myArray = buildArray(); // type: (number | boolean)[]
// Tuple
const t1 = ["Bob", "Smith", 21];
t1[0] = "Catherine"; // Element of a tuple is mutable
// Read-only array
let a1 = [1, 2, 3];
function speak(l) {
    return "Spoken";
}
speak("Russian" /* Language.Russian */);
// Named function
function add(a, b) {
    return a + b;
}
const result = add(2, 3);
// Function expression
let add2 = function (a, b) {
    return a + b;
};
// Arrow function expression
let add3 = (a, b) => {
    return a + b;
};
// Shorthand arrow function expression
let add4 = (a, b) => a + b;
// Function constructor -- unsafe
let add5 = new Function('a', 'b', 'return a+b');
// console.log(add5(4,5)); // 9
// Default parameter
function log(message, userId) {
    console.log(new Date().toLocaleDateString(), message, userId || 'No user');
}
// Variadic function
function sumVariadic(...numbers) {
    return numbers.reduce((total, n) => total + n, 0);
}
// Call, bind, apply
console.assert(add2.apply(null, [10, 20]) === 30);
console.assert(add2.call(null, 10, 20) === 30);
console.assert(add2.bind(null, 10, 20)() === 30);
// this
// The function formatDate doesn't take any parameters
function formatDate() {
    return `${this.getDate()}-${this.getMonth()}-${this.getFullYear()}`;
}
console.log(formatDate.call(new Date));
// Generator function
function* bernoulliSamples(p) {
    while (true) {
        if (Math.random() <= p) {
            yield 1;
        }
        else {
            yield 0;
        }
    }
}
let bernoulli = bernoulliSamples(0.4);
console.log(bernoulli.next());
//# sourceMappingURL=index.js.map