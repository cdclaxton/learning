// Named function
function foo(x) {
    console.log("foo(): " + x);
}

// Anonymous function
const foo2 = function(x) {
    console.log("foo2(): " + x);
}

// Single-line arrow function (implicit return statement)
const greeting = (subject) =>  `Hello ${subject}`;
console.log(greeting("Chris"));

// Arrow function
const foo3 = (x) => {
    console.log("foo3(): " + x);
}

// Arrow function with default parameters
const defaultGreeting = (greeting, subject="Chris") => `${greeting} ${subject}`;
console.log(defaultGreeting("Evening"));

foo(3);
foo2(4);
foo3(5);

// Immediately Invoked Function Expression (IIFE)
(function test() {
    console.log("test(): IIFE");
})();

// IIFEs can return values
var x = (function IIFE() {
    return 42;
})();
console.log(x);

// Rest parameter
const max = function(...values) {
    console.log(values instanceof Array);

    let largest = values[0];
    for (let i=1; i<values.length; i++) {
        largest = values[i] > largest ? values[i] : largest;
    }
    return largest
}
console.log("max value = " + max(0, 4, 2));

// Default function parameters
const fetchData = function(id, location={host: 'localhost', port: 443}, 
    uri='employees') {
    url = "https://" + location.host + ":" + location.port  + "/" + uri +
        "/" + id;
    console.log(url);
}
fetchData(4);
fetchData(5, location=undefined, uri='bank')

// Expressions as default parameters
const computeTax = function(amount, stateTax=14, localTax=stateTax*0.1) {
    const total = amount + amount * (stateTax + localTax) / 100;
    console.log(`Amount: ${amount}, Total: ${total}`);
}
computeTax(100);

// Currying
const sayHi = defaultGreeting.bind(null, "Hi");
console.log(sayHi("Dave"));

// Filter, map and join
const pickNames = function(names, length) {
    return names.
        filter((name) => name.length === length).
        map((name) => name.toUpperCase()).
        join(", ")
}
console.log(pickNames(["Chris", "Dave", "Samantha", "James"], 5));

// Generators
// Class to represent an effects chain
class EffectsChain {
    constructor() {
        this.mainEffects = ["Overdrive", "Modulation", "Delay", "Reverb"];
        this.modulationEffects = ["Flanger", "Chorus", "Phaser"];
    }
    
    // Define a generator
    *main() {
        for (const effect of this.mainEffects) {
            yield effect;
        }
    }
    
    // Define another generator
    *modulation() {
        for (const effect of this.modulationEffects) {
            yield effect;
        }
    }
    
    // Combine generators
    *mainAndModulation() {
        yield* this.main();
        yield* this.modulation();
    }
}
    
const effects = new EffectsChain();

console.log("Main effects:");
for (const effect of effects.main()) {
    console.log(effect);
}

console.log("\nAll effects:");
for (const effect of effects.mainAndModulation()) {
    console.log(effect);
}

// Iterator
class ChristmasLights {
    constructor() {
        this.lights = ["red", "green", "blue", "yellow"];
    }

    // Decorate a method with * to denote that the iterator uses a 'yield'
    *[Symbol.iterator]() {
        for (const light of this.lights) {
            yield light;
        }
    }
}

const lightCircuit = new ChristmasLights();
for (light of lightCircuit) {
    console.log(`Christmas light: ${light}`);
}

// Closures
function makeAdder(x) {
    // Inner function add() uses x, so the function has a closure over it
    function add(y) {
        return y + x;
    }
    return add;
}
const plusOne = makeAdder(1);
console.log(plusOne(10));