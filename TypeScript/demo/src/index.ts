import { assert } from "console";

console.log("Hello TypeScript!");

// Unknown
let u: unknown = 30
if (typeof u === 'number') {
    //console.log(u);  // 30
}

// Symbol
let symbol1: symbol = Symbol('s');
let symbol2: symbol = Symbol('s');
console.assert(symbol1 != symbol2);

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

// Type union -- a value with a union type can be both members at once
type FreightTrain = {reg: string, maxTrucks: number};
type PassengerTrain = {reg: string, numPassengers: number};
type FreightOrPassengerTrain = FreightTrain | PassengerTrain;
type FreightAndPassengerTrain = FreightTrain & PassengerTrain;

// PassengerTrain
let freightOrPassengerTrain: FreightOrPassengerTrain = {
    reg: "P1190",
    numPassengers: 350,
}

let freightAndPassengerTrain: FreightAndPassengerTrain = {
    reg: "Y101",
    numPassengers: 125,
    maxTrucks: 5,
}
// console.log(freightAndPassengerTrain); // { reg: 'Y101', numPassengers: 125, maxTrucks: 5 }

// Class
class Person {
    constructor(
        public firstName: string, // equivalent to this.firstName = firstName
        public lastName: string,
    ) {}
}

const c = new Person("Bob", "Smith");

// Arrays
let array1: number[] = [1,2,3];
let array2: (number|boolean)[] = [1, true, 3];
let array3: Array<string> = ["Bob", "Sarah"];

let array4 = [1, true]; // (number|string)[]
let array5 = array4.map(_ => {
    if (typeof _ === 'number') {
        return _ * 2;
    }
    return !_;
})
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
const t1: [string, string, number] = ["Bob", "Smith", 21];
t1[0] = "Catherine";  // Element of a tuple is mutable

// Read-only array
let a1: readonly number[] = [1, 2, 3];
let b1: readonly number[] = a1.concat(4);
// console.log(b1); // [ 1, 2, 3, 4 ]

// Enum
const enum Language {
    Russian = 'Russian',
    English = 'English'
}

function speak(l: Language) {
    return "Spoken: " + l;
}
speak(Language.Russian); // Spoken: Russian
speak(Language['Russian']);

// Enums can mix string and number values
enum Colour {
    Red = '#c10000',
    White = 255,
}
// console.log(Colour.Red); // #c10000
// console.log(Colour.White); // 255

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

// Function constructor -- unsafe (parameters and return type are untyped)
let add5 = new Function('a', 'b', 'return a+b');
console.assert(add5(4,5) === 9);

// Optional parameter
function log(message: string, userId?: string) {
    console.log(new Date().toLocaleDateString(), message, userId || 'No user');
}

// Default parameter
function add6(a: number, b: number = 10): number {
    return a + b;
}
console.assert(add6(5) === 15);

// Variadic function
function sumVariadic(...numbers: number[]): number {
    return numbers.reduce((total, n) => total + n, 0);
}
console.assert(sumVariadic(1,2,3) === 6);

// Call, bind, apply
console.assert(add2.apply(null, [10, 20]) === 30);
console.assert(add2.call(null, 10, 20) === 30);
console.assert(add2.bind(null, 10, 20)() === 30);

// this
// The function formatDate doesn't take any parameters
// A Date has to be bound to the function call, otherwise a TypeError occurs
function formatDate(this: Date) {
    return `${this.getDate()}-${this.getMonth()}-${this.getFullYear()}`;
}
// console.log(formatDate.call(new Date)) // 26-6-2024

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
// console.log(bernoulli.next()); // { value: 0, done: false }

// numbersTo10 is an iterable
let numbersTo10 = {
    *[Symbol.iterator]() {
        for (let i=0; i<10; i++) {
            yield i;
        }
    }
}
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
// console.log('one:', one); // one: 0
// console.log('two:', two); // two: 1
// console.log('rest:', rest); // rest: [2, 3, 4, 5, 6, 7, 8, 9]

// Call signature
type Log = (message: string, userId?: string) => void;

// Function expression that implements a signature
let logger: Log = (message, userId = 'Not signed in') => {
    let time = new Date().toISOString();
    console.log(time, message, userId);
}
// logger("Function created");  // 2024-07-27T19:58:53.215Z Function created Not signed in

// -----------------------------------------------------------------------------
// Overloading functions
// -----------------------------------------------------------------------------

// Overloaded function
type ScheduleRoute = {
    (reg: string, numCars: number): string // Passenger
    (reg: string, freightType: string, numWagons: number): string // Freight
}

let routeScheduler: ScheduleRoute = (
    reg: string,
    numCarsOrFreightType: number|string,
    numWagons?:number
): string => {
    // Passenger
    if (typeof numCarsOrFreightType === 'number') {
        return `Passenger train reg ${reg} as ${numCarsOrFreightType} cars`;
    } else if (typeof numCarsOrFreightType === 'string') {
        return `Freight train reg ${reg} carrying ${numCarsOrFreightType} in ${numWagons} wagons`;
    }
    return "";
}
console.assert(routeScheduler("X102", 10) === 'Passenger train reg X102 as 10 cars');
console.assert(routeScheduler("X231", "coal", 25) === 'Freight train reg X231 carrying coal in 25 wagons');

// Overloaded function expressions
type Train = string;
type CreateTrain = {
    (type: 'freight'): Train,
    (type: 'passenger'): Train
}
let createTrain: CreateTrain = (type: string): Train => {
    return `${type} train`; 
}
console.assert(createTrain('freight') === 'freight train');
console.assert(createTrain('passenger') === 'passenger train');
// createTrain('eurostar') // <-- no overload matches this call

// Overload function definition
function makeWagon(type: 'oil'): string;
function makeWagon(type: 'coal'): string;
function makeWagon(type: string): string {
    return `${type} wagon`;
}
console.assert(makeWagon('coal') === 'coal wagon');

// -----------------------------------------------------------------------------
// Function properties
// -----------------------------------------------------------------------------

function mailTrainAlerter(reg: string): string {
    if (mailTrainAlerter.setToReady) {
        return "mail train is already ready";
    }
    mailTrainAlerter.setToReady = true;
    return `mail train ${reg} is ready`
}
mailTrainAlerter.setToReady = false;

console.assert(mailTrainAlerter('M101') === "mail train M101 is ready");
console.assert(mailTrainAlerter('M101') === "mail train is already ready");

// -----------------------------------------------------------------------------
// Polymorphism
// -----------------------------------------------------------------------------

type Filter = {
    <T>(array: T[], f: (item:T) => boolean): T[]
}
let filter: Filter = (array, f) => {
    let result = [];
    for (let i = 0; i < array.length; i++) {
        let item = array[i];
        if (f(item)) {
            result.push(item);
        }
    }
    return result;
}

// console.log(filter([1,2,3,4], _ => _ < 3)); // [1,2]

let filter2 = <T>(array: T[], f: (item: T) => boolean): T[] => {
    let result: T[] = [];
    for (let i = 0; i < array.length; i++) {
        let item = array[i];
        if (f(item)) {
            result.push(item);
        }
    }
    return result;
}

// console.log(filter2([1,2,3,4], _ => _ < 3)); // [1,2]

// Scope T to the type alias
type Filter2<T> = {
    (array: T[], f: (item:T) => boolean): T[]
}
let stringFilter: Filter2<string> = (array, f) => {
    return array.filter(f)
}
console.assert(stringFilter(["a", "bb", "ccc"], _ => _.length <= 2).toString() === "a,bb");

function map<T,U>(array: T[], f: (item:T) => U): U[] {
    let result = [];
    for (let i=0; i<array.length; i++) {
        result[i] = f(array[i]);
    }
    return result;
}

// Generic types are inferred
console.assert(map([1,2,3], _ => (2*_).toString()).toString() === "2,4,6");

// Generic types are explicitly defined
console.assert(map<number,string>([1,2,3], _ => (2*_).toString()).toString() === "2,4,6");

// Generic type alias
type WagonLoad<T> = {
    id: number
    load: T
};
function fillWagon<T>(load: WagonLoad<T>): string {
    return `Wagon with id ${load.id} filled with ${load.load}`;
}
console.assert(
    fillWagon<string>({
        id: 8,
        load: "coal",
    }) === 'Wagon with id 8 filled with coal');

// -----------------------------------------------------------------------------
// Bounded polymorphism (with multiple constraints)
// -----------------------------------------------------------------------------

type HasMass = {
    mass: number,
}
type HasVelocity = {
    velocity: number,
}
function kineticEnergy<
    MovingObject extends HasMass & HasVelocity
>(m: MovingObject): number {
    return 0.5 * m.mass * m.velocity * m.velocity;
}

type MovingTrain = HasMass & HasVelocity;
let movingTrain: MovingTrain = {
    mass: 500,
    velocity: 10,
}
console.assert(kineticEnergy(movingTrain) === 25000);

// -----------------------------------------------------------------------------
// Classes
// -----------------------------------------------------------------------------

// Types to represent the valid positions on the board
type File = 'A' | 'B' | 'C';
type Rank = 1 | 2 | 3;

type DistanceSelector = (d: number) => boolean;
let distanceEqualTo1: DistanceSelector = (d: number): boolean => {
    return d === 1;
}


class Position {
    static allFiles: File[] = ['A', 'B', 'C'];
    static allRanks: Rank[] = [1, 2, 3];

    constructor(private file: File, private rank: Rank) {}

    moveTo(file: File, rank: Rank) {
        this.file = file;
        this.rank = rank;
    }

    static manhattanDistance(p1: Position, p2: Position): number {
        let fileDistance = Math.abs(p1.file.charCodeAt(0) - p2.file.charCodeAt(0));
        let rankDistance = Math.abs(p1.rank - p2.rank);
        return fileDistance + rankDistance;        
    }

    otherPositionsMatching(fn: DistanceSelector): Position[] {
        let positions: Position[] = [];
        for (let f of Position.allFiles) {
            for (let r of Position.allRanks) {
                let potential = new Position(f, r);
                if (fn(Position.manhattanDistance(this, potential))) {
                    positions.push(potential);
                }
            }
        }
        return positions
    }

    equal(p: Position): boolean {
        return this.file === p.file && this.rank === p.rank;
    }
}

abstract class Agent {
    protected position: Position;
    protected otherAgent: Agent | undefined;
    
    constructor(initial: Position) {
        this.position = initial;
    }

    public setOtherAgent(other: Agent) {
        this.otherAgent = other;
    }

    private potentialMovesByOtherAgent(): Position[] {
        if (this.otherAgent === undefined) {
            return [];
        }
        let otherAgentMoves = this.otherAgent.position.otherPositionsMatching(distanceEqualTo1);
        otherAgentMoves.push(this.otherAgent.position);
        return otherAgentMoves;
    }

    public potentialMovesAwayFromOtherAgent(): Position[] {
        let myPotentialMoves = this.position.otherPositionsMatching(distanceEqualTo1);
        let otherAgentPotentialMoves = this.potentialMovesByOtherAgent();

        let result: Position[] = [];
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
    constructor(private name: string, initial: Position) {
        super(initial);
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
    protected values: number[] = [];
    addValue(v: number): this {
        this.values.push(v);
        return this;
    }
}

class C2 extends C1 {
    total(): number {
        return this.values.reduce((a, b) => a + b, 0);
    }
}

let c2Obj = new C2();
c2Obj.addValue(2).addValue(4);
console.assert(c2Obj.total() === 6);

// -----------------------------------------------------------------------------
// Interfaces
// -----------------------------------------------------------------------------

interface Animal {
    readonly name: string
    eat(food: string): string
}

class Cat implements Animal {
    constructor(public readonly name: string) {}
    eat(food: string): string {
        return `${this.name} is enjoying ${food}`;
    }
}

let kiki = new Cat("Kiki");
console.assert(kiki.eat("biscuits") === "Kiki is enjoying biscuits");

// -----------------------------------------------------------------------------
// Classes are structurally typed
// -----------------------------------------------------------------------------

class C3 {
    move(): void {}
}

class C4 {
    move(): void {}
}

let mover = (c: C3): void => {
    c.move()
}

mover(new C3);
mover(new C4);  // Note how a C3 was expected, but a C4 can be passed in

// -----------------------------------------------------------------------------
// Factory pattern
// -----------------------------------------------------------------------------

type Crayon = {
    colour: string
}

class RedCrayon implements Crayon {
    colour = "red";
}

class GreenCrayon implements Crayon {
    colour = "green";
}

// Companion object
let Crayon = {
    create(type: 'red' | 'green'): Crayon {
        switch (type) {
            case 'red': return new RedCrayon
            case 'green': return new GreenCrayon
        }
    }
}

console.assert(Crayon.create('red').colour === 'red');

// -----------------------------------------------------------------------------
// Builder pattern
// -----------------------------------------------------------------------------

class HotAirBalloon {
    private numGasCanisters: number | null = null;
    private basketCapacity: number | null = null;

    setNumGasCanisters(n: number): this {
        this.numGasCanisters = n;
        return this;
    }

    setBasketCapacity(n: number): this {
        this.basketCapacity = n;
        return this;
    }

    describe(): string {
        return `Built a hot air balloon with ${this.numGasCanisters} canisters to carry ${this.basketCapacity} people`;
    }
}

console.assert(
    new HotAirBalloon().setBasketCapacity(12).setNumGasCanisters(4).describe() ===
    "Built a hot air balloon with 4 canisters to carry 12 people")

// -----------------------------------------------------------------------------
// Sets
// -----------------------------------------------------------------------------

class Employee {
    constructor(public name: string) {}
}
let emp1 = new Employee("Bob");
let emp2 = new Employee("Sarah");
let employees = new Set([emp1, emp2]);
console.assert(employees.has(emp1));

let emp3 = new Employee("Bob");  // Same as emp1
console.assert(!employees.has(emp3));
