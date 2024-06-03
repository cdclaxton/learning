// 
class Rectangle {
    // Class fields
    height = 0;
    width;

    // Private property
    #largestSide = 0;

    static name = "Rectangle";  // static field

    // Constructor method
    constructor(height, width) {
        this.height = height;
        this.width = width;
        this.#largestSide = height > width ? height : width;
    }

    // Method
    calcArea() {
        return this.height * this.width;
    }
    
    // Getter
    get area() {
        return this.calcArea();
    }

    largestSide() {
        return this.#largestSide;
    }

    // Iterator
    *getSides() {
        yield this.height;
        yield this.width;
    }

    // Static method
    static square(a) {
        return new Rectangle(a, a);
    }
}

const r = new Rectangle(10, 6);
console.log(`Rectangle area: ${r.area}`)  // Rectangle area: 60
console.log([...r.getSides()]);  // [ 10, 6 ]
console.log(Rectangle.name);  // Rectangle
console.log(`Largest side: ${r.largestSide()}`)  // Largest side: 10

s = Rectangle.square(3);
console.log(`Square area: ${s.area}`);  // Square area: 9

class Shape {
    constructor(name, numSides) {
        this.name = name;
        this.numSides = numSides;
    }

    describe() {
        return `A ${this.name} has ${this.numSides} sides`;
    }
}

class Square extends Shape {
    constructor(length) {
        super("square", 4); // call super class constructor
        this.length = length;
    }

    describe() {
        return super.describe() + ", " + `length: ${this.length}`;
    }
}

const sq = new Square(3);
console.log(sq.describe());  // A square has 4 sides, length: 3

// Create an object using a normal function
const createNewPerson = (name) => {
    return {
        name: name,
        greeting: function () {
            return `Hi, I'm ${this.name}`;
        }
    }
}

let p1 = createNewPerson("Bob");
console.log(p1);
console.log(p1.greeting()); // Hi, I'm Bob

// Constructor function (JavaScript version of a class)
// This defines the 'greeting' function every time, which is not ideal
function Person(name) {
    this.name = name;
    this.greeting = function() { return "Hi, I'm " + this.name };
}

let p2 = new Person("Dave");  // note the 'new' keyword
console.log(`p2: ${p2.greeting()}`); // Hi, I'm Dave

// Using the Object constructor
let p3 = new Object();
p3.name = "Sandra";
p3.greeting = function() {
    return "Hi, I'm " + this.name
};
console.log(p3);
console.log(`p3: ${p3.greeting()}`); // Hi, I'm Sandra

// Using the Object constructor with parameters
let p4 = new Object({
    name: "Dave",
    greeting: function() { return "Hi, I'm " + this.name; }
});
console.log(`p4: ${p4.greeting()}`); // Hi, I'm Dave

// Create a new object based on an existing object (based on a prototype objet)
let p5 = Object.create(p1);
p5.name = "Robert";
console.log(`p5: ${p5.greeting()}`); // Hi, I'm Robert
