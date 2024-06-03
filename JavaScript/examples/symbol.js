// Symbol created by each call is unique
const nameTom = 'Tom';
let nameTom1 = Symbol(nameTom);
let nameTom2 = Symbol(nameTom);

console.log(nameTom1); // Symbol(Tom)
console.log("type of nameTom1 = " + typeof(nameTom1)); // type of nameTom1 = symbol
console.log(nameTom1 === nameTom2); // false

// Use a Symbol to create a property
const age = Symbol('ageValue'); // creates a unique Symbol (arg. is for debugging purposes)
const email = 'emailValue'; // string
const dave = {
    first: 'Dave',
    [email]: 'dave@example.com', // create a property --> emailValue: 'dave@example.com'
    [age]: 2 // define a property of type Symbol
};

// {
//     first: 'Dave',
//     emailValue: 'dave@example.com',
//     [Symbol(ageValue)]: 2
// }
console.log(dave);

// Iterate over the properties
// (note 'age' is not exposed due to being of type Symbol)
// first: Dave
// emailValue: dave@example.com
for (const property in dave) {
    console.log(property + ": " + dave[property]);
}

// Query for all property names (note ageValue is not exposed due to being of type Symbol)
console.log(Object.getOwnPropertyNames(dave)); // [ 'first', 'emailValue' ]
console.log(Object.getOwnPropertySymbols(dave)); // [ Symbol(ageValue) ]

// To access a Symbol property
console.log("age = " + dave[age]); // age = 2
dave[age] = 3;
console.log("age = " + dave[age]); // age = 3

// Symbol.for(<key>) method creates a Symbol if one doesn't already exist for that key in the
// global registry and creates a new instance or it returns the pre-existing one
const masterWizard = Symbol.for("Dumbledore");
const topWizard = Symbol.for("Dumbledore");

console.log(typeof(masterWizard)); // symbol
console.log(masterWizard); // Symbol(Dumbledore)
console.log(masterWizard === topWizard); // true

// Get the key associated with a Symbol in the registry
console.log('Dumbledore' === Symbol.keyFor(topWizard)); // true

// .search() method example
console.log("Search examples ...")
console.log("Chris".search("Chris")); // 0
console.log("Chris".search("Christopher")); // -1
console.log("Chris".search("Dave")); // -1
console.log("Chris".search("is")); // 3

// Define a class with a search() method
class SuperHero {
    constructor(name, realName) {
        this.name = name;
        this.realName = realName;
    }

    toString() { return this.name; }

    [Symbol.search](value) {
        return value.search(this.realName);
    }
}

const superHeroes = [new SuperHero('Superman', 'Clark Kent'), 
    new SuperHero('Batman', 'Bruce Wayne')];

for (const s of superHeroes) {
    console.log(`Super hero: ${s}`);
}