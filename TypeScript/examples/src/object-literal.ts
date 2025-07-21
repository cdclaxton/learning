let p1 = {
    firstName: "Bob",
    surname: "Smith"
}

class Person {
    constructor(
        public firstName: string,
        public surname: string
    ) {}
}

// A Person object is assignable to p1 because it has the same shape
p1 = new Person('Sally', 'Davies');
console.log(p1);

let p2: {
    firstName: string,
    surname: string,
    age?: number // optional
}

p2 = new Person('Matt', 'Davies');
console.log(p2);

// An object literal with a method
let user: {
    readonly name: string, // read-only property
    lastLogin: string
    toString(): string // method
} = {
    name: "Bob Smith",
    lastLogin: "2025-07-13",
    toString() {
        return `${this.name} -- last login on ${this.lastLogin}`
    }
}
console.log(user.toString());

// Empty object -- don't use
let danger: {};
danger = {x: 1};

