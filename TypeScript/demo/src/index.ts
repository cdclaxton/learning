import { assert } from "console";

console.log("Hello TypeScript!");

// Declare a type alias
type Age = number;

// Declare an object literal with a given 'shape'
let a: {
    readonly b:string // Read-only field
    c?: string // Optional
    [key:number]: boolean // Using an index signature
    d: Age // Using a type alias
} = {
    b: 'x',
    20: true,
    30: false,
    d: 21,
}

// Class
class Person {
    constructor(
        public firstName: string, // equivalent to this.firstName = firstName
        public lastName: string,
    ) {}
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
const t1: [string, string, number] = ["Bob", "Smith", 21];
t1[0] = "Catherine";  // Element of a tuple is mutable

// Read-only array
let a1: readonly number[] = [1, 2, 3];

// Enum
const enum Language {
    Russian = 'Russian',
    English = 'English'
}

function speak(l: Language) {
    return "Spoken";
}
speak(Language.Russian);

// Named function
function add(a: number, b: number): number {
    return a + b;
}
const result = add(2,3);

// Function expression
let add2 = function(a: number, b: number): number {
    return a + b;
};

// Arrow function expression
let add3 = (a: number, b: number): number => {
    return a + b;
}

// Shorthand arrow function expression
let add4 = (a: number, b: number) => a + b;

// Function constructor -- unsafe
let add5 = new Function('a', 'b', 'return a+b');
// console.log(add5(4,5)); // 9

// Default parameter
function log(message: string, userId?: string) {
    console.log(new Date().toLocaleDateString(), message, userId || 'No user');
}

// Variadic function
function sumVariadic(...numbers: number[]): number {
    return numbers.reduce((total, n) => total + n, 0);
}

// Call, bind, apply
console.assert(add2.apply(null, [10, 20]) === 30);
console.assert(add2.call(null, 10, 20) === 30);
console.assert(add2.bind(null, 10, 20)() === 30);

// this
// The function formatDate doesn't take any parameters
function formatDate(this: Date) {
    return `${this.getDate()}-${this.getMonth()}-${this.getFullYear()}`;
}
console.log(formatDate.call(new Date))

// Generator function
function* bernoulliSamples(p: number): IterableIterator<number> {
    while (true) {
        if (Math.random() <= p) {
            yield 1;
        } else {
            yield 0;
        }
    }
}
let bernoulli = bernoulliSamples(0.4);
console.log(bernoulli.next());