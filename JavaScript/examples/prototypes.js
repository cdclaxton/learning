// Constructor function
function Animal(name, age) {
    this.name = name;
    this.age = age;
    this.about = function() { return "I'm a " + this.name + " and I'm " + this.age + " years old!"; }
}

let animal1 = new Animal("Giraffe", 4);
console.log(animal1.about());

// Use the constructor function (useful if there isn't a reference to the original constructor)
let animal2 = new animal1.constructor("Frog", 1);
console.log(animal2.about());

// Get the name of the constructor
console.log(animal2.constructor.name);

// Modify the prototype
Animal.prototype.farewell = function() { return "Bye bye " + this.name };
console.log(animal2.farewell());
console.log(animal1.farewell());