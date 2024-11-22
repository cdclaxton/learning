"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
console.log("Hello TypeScript!");
// Unknown
let u = 30;
if (typeof u === 'number') {
    //console.log(u);  // 30
}
// Symbol
let symbol1 = Symbol('s');
let symbol2 = Symbol('s');
console.assert(symbol1 != symbol2);
// Declare an object literal with a given 'shape'
let a = {
    b: 'x',
    20: true,
    30: false,
    d: 21,
};
// PassengerTrain
let freightOrPassengerTrain = {
    reg: "P1190",
    numPassengers: 350,
};
let freightAndPassengerTrain = {
    reg: "Y101",
    numPassengers: 125,
    maxTrucks: 5,
};
// console.log(freightAndPassengerTrain); // { reg: 'Y101', numPassengers: 125, maxTrucks: 5 }
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
let array1 = [1, 2, 3];
let array2 = [1, true, 3];
let array3 = ["Bob", "Sarah"];
let array4 = [1, true]; // (number|string)[]
let array5 = array4.map(_ => {
    if (typeof _ === 'number') {
        return _ * 2;
    }
    return !_;
});
// console.log(array5); // [ 2, false ]
// Arrays -- once an array leaves the scope in which it was defined, TypeScript
// will assign it a final type (that can't be expanded)
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
let b1 = a1.concat(4);
function speak(l) {
    return "Spoken: " + l;
}
speak("Russian" /* Language.Russian */); // Spoken: Russian
speak("Russian" /* Language['Russian'] */);
// Enums can mix string and number values
var Colour;
(function (Colour) {
    Colour["Red"] = "#c10000";
    Colour[Colour["White"] = 255] = "White";
})(Colour || (Colour = {}));
// console.log(Colour.Red); // #c10000
// console.log(Colour.White); // 255
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
// Function constructor -- unsafe (parameters and return type are untyped)
let add5 = new Function('a', 'b', 'return a+b');
console.assert(add5(4, 5) === 9);
// Optional parameter
function log(message, userId) {
    console.log(new Date().toLocaleDateString(), message, userId || 'No user');
}
// Default parameter
function add6(a, b = 10) {
    return a + b;
}
console.assert(add6(5) === 15);
// Variadic function
function sumVariadic(...numbers) {
    return numbers.reduce((total, n) => total + n, 0);
}
console.assert(sumVariadic(1, 2, 3) === 6);
// Call, bind, apply
console.assert(add2.apply(null, [10, 20]) === 30);
console.assert(add2.call(null, 10, 20) === 30);
console.assert(add2.bind(null, 10, 20)() === 30);
// this
// The function formatDate doesn't take any parameters
// A Date has to be bound to the function call, otherwise a TypeError occurs
function formatDate() {
    return `${this.getDate()}-${this.getMonth()}-${this.getFullYear()}`;
}
// console.log(formatDate.call(new Date)) // 26-6-2024
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
// console.log(bernoulli.next()); // { value: 0, done: false }
// numbersTo10 is an iterable
let numbersTo10 = {
    *[Symbol.iterator]() {
        for (let i = 0; i < 10; i++) {
            yield i;
        }
    }
};
let total2 = 0;
for (let n of numbersTo10) {
    total2 += n;
}
// console.log(total2); // 45
// Spread an iterator
let allNumbersTo10 = [...numbersTo10];
// console.log(allNumbersTo10); // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
// Destructure an iterator
let [one, two, ...rest] = numbersTo10;
// Function expression that implements a signature
let logger = (message, userId = 'Not signed in') => {
    let time = new Date().toISOString();
    console.log(time, message, userId);
};
let routeScheduler = (reg, numCarsOrFreightType, numWagons) => {
    // Passenger
    if (typeof numCarsOrFreightType === 'number') {
        return `Passenger train reg ${reg} as ${numCarsOrFreightType} cars`;
    }
    else if (typeof numCarsOrFreightType === 'string') {
        return `Freight train reg ${reg} carrying ${numCarsOrFreightType} in ${numWagons} wagons`;
    }
    return "";
};
console.assert(routeScheduler("X102", 10) === 'Passenger train reg X102 as 10 cars');
console.assert(routeScheduler("X231", "coal", 25) === 'Freight train reg X231 carrying coal in 25 wagons');
let createTrain = (type) => {
    return `${type} train`;
};
console.assert(createTrain('freight') === 'freight train');
console.assert(createTrain('passenger') === 'passenger train');
function makeWagon(type) {
    return `${type} wagon`;
}
console.assert(makeWagon('coal') === 'coal wagon');
// -----------------------------------------------------------------------------
// Function properties
// -----------------------------------------------------------------------------
function mailTrainAlerter(reg) {
    if (mailTrainAlerter.setToReady) {
        return "mail train is already ready";
    }
    mailTrainAlerter.setToReady = true;
    return `mail train ${reg} is ready`;
}
mailTrainAlerter.setToReady = false;
console.assert(mailTrainAlerter('M101') === "mail train M101 is ready");
console.assert(mailTrainAlerter('M101') === "mail train is already ready");
let filter = (array, f) => {
    let result = [];
    for (let i = 0; i < array.length; i++) {
        let item = array[i];
        if (f(item)) {
            result.push(item);
        }
    }
    return result;
};
// console.log(filter([1,2,3,4], _ => _ < 3)); // [1,2]
let filter2 = (array, f) => {
    let result = [];
    for (let i = 0; i < array.length; i++) {
        let item = array[i];
        if (f(item)) {
            result.push(item);
        }
    }
    return result;
};
let stringFilter = (array, f) => {
    return array.filter(f);
};
console.assert(stringFilter(["a", "bb", "ccc"], _ => _.length <= 2).toString() === "a,bb");
function map(array, f) {
    let result = [];
    for (let i = 0; i < array.length; i++) {
        result[i] = f(array[i]);
    }
    return result;
}
// Generic types are inferred
console.assert(map([1, 2, 3], _ => (2 * _).toString()).toString() === "2,4,6");
// Generic types are explicitly defined
console.assert(map([1, 2, 3], _ => (2 * _).toString()).toString() === "2,4,6");
function fillWagon(load) {
    return `Wagon with id ${load.id} filled with ${load.load}`;
}
console.assert(fillWagon({
    id: 8,
    load: "coal",
}) === 'Wagon with id 8 filled with coal');
function kineticEnergy(m) {
    return 0.5 * m.mass * m.velocity * m.velocity;
}
let movingTrain = {
    mass: 500,
    velocity: 10,
};
console.assert(kineticEnergy(movingTrain) === 25000);
let distanceEqualTo1 = (d) => {
    return d === 1;
};
class Position {
    constructor(file, rank) {
        this.file = file;
        this.rank = rank;
    }
    moveTo(file, rank) {
        this.file = file;
        this.rank = rank;
    }
    static manhattanDistance(p1, p2) {
        let fileDistance = Math.abs(p1.file.charCodeAt(0) - p2.file.charCodeAt(0));
        let rankDistance = Math.abs(p1.rank - p2.rank);
        return fileDistance + rankDistance;
    }
    otherPositionsMatching(fn) {
        let positions = [];
        for (let f of Position.allFiles) {
            for (let r of Position.allRanks) {
                let potential = new Position(f, r);
                if (fn(Position.manhattanDistance(this, potential))) {
                    positions.push(potential);
                }
            }
        }
        return positions;
    }
    equal(p) {
        return this.file === p.file && this.rank === p.rank;
    }
}
Position.allFiles = ['A', 'B', 'C'];
Position.allRanks = [1, 2, 3];
class Agent {
    constructor(initial) {
        this.position = initial;
    }
    setOtherAgent(other) {
        this.otherAgent = other;
    }
    potentialMovesByOtherAgent() {
        if (this.otherAgent === undefined) {
            return [];
        }
        let otherAgentMoves = this.otherAgent.position.otherPositionsMatching(distanceEqualTo1);
        otherAgentMoves.push(this.otherAgent.position);
        return otherAgentMoves;
    }
    potentialMovesAwayFromOtherAgent() {
        let myPotentialMoves = this.position.otherPositionsMatching(distanceEqualTo1);
        let otherAgentPotentialMoves = this.potentialMovesByOtherAgent();
        let result = [];
        for (let move of myPotentialMoves) {
            let found = false;
            for (let otherMove of otherAgentPotentialMoves) {
                if (move.equal(otherMove)) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                result.push(move);
            }
        }
        return result;
    }
}
class Tank extends Agent {
    constructor(name, initial) {
        super(initial);
        this.name = name;
    }
}
let tank1 = new Tank("Tank-1", new Position('A', 1));
let tank2 = new Tank("Tank-2", new Position('A', 2));
tank1.setOtherAgent(tank2);
tank2.setOtherAgent(tank1);
console.assert(tank2.potentialMovesAwayFromOtherAgent().length === 2);
// -----------------------------------------------------------------------------
// Using 'this' as a return type
// -----------------------------------------------------------------------------
class C1 {
    constructor() {
        this.values = [];
    }
    addValue(v) {
        this.values.push(v);
        return this;
    }
}
class C2 extends C1 {
    total() {
        return this.values.reduce((a, b) => a + b, 0);
    }
}
let c2Obj = new C2();
c2Obj.addValue(2).addValue(4);
console.assert(c2Obj.total() === 6);
class Cat {
    constructor(name) {
        this.name = name;
    }
    eat(food) {
        return `${this.name} is enjoying ${food}`;
    }
}
let kiki = new Cat("Kiki");
console.assert(kiki.eat("biscuits") === "Kiki is enjoying biscuits");
// -----------------------------------------------------------------------------
// Classes are structurally typed
// -----------------------------------------------------------------------------
class C3 {
    move() { }
}
class C4 {
    move() { }
}
let mover = (c) => {
    c.move();
};
mover(new C3);
mover(new C4); // Note how a C3 was expected, but a C4 can be passed in
class RedCrayon {
    constructor() {
        this.colour = "red";
    }
}
class GreenCrayon {
    constructor() {
        this.colour = "green";
    }
}
// Companion object
let Crayon = {
    create(type) {
        switch (type) {
            case 'red': return new RedCrayon;
            case 'green': return new GreenCrayon;
        }
    }
};
console.assert(Crayon.create('red').colour === 'red');
// -----------------------------------------------------------------------------
// Builder pattern
// -----------------------------------------------------------------------------
class HotAirBalloon {
    constructor() {
        this.numGasCanisters = null;
        this.basketCapacity = null;
    }
    setNumGasCanisters(n) {
        this.numGasCanisters = n;
        return this;
    }
    setBasketCapacity(n) {
        this.basketCapacity = n;
        return this;
    }
    describe() {
        return `Built a hot air balloon with ${this.numGasCanisters} canisters to carry ${this.basketCapacity} people`;
    }
}
console.assert(new HotAirBalloon().setBasketCapacity(12).setNumGasCanisters(4).describe() ===
    "Built a hot air balloon with 4 canisters to carry 12 people");
// -----------------------------------------------------------------------------
// Sets
// -----------------------------------------------------------------------------
class Employee {
    constructor(name) {
        this.name = name;
    }
}
let emp1 = new Employee("Bob");
let emp2 = new Employee("Sarah");
let employees = new Set([emp1, emp2]);
console.assert(employees.has(emp1));
let emp3 = new Employee("Bob"); // Same as emp1
console.assert(!employees.has(emp3));
//# sourceMappingURL=index.js.map