// Anonymous function that returns an array of arguments
const getVehicle = function() {
    return ['Hyundai', 'i30', 'Blue'];
};
    
// Get each of the elements returned as variables
const [make, model, colour] = getVehicle();
console.log(`Make: ${make}; Model: ${model}; Colour: ${colour}`);

// Ignore 'make'
const [make2,, colour2] = getVehicle();
console.log(`Make: ${make2}; Colour: ${colour2}`);

// Using default values
const [make3, model3, colour3, reg3='Unknown'] = getVehicle();
console.log(`Make: ${make3}; Model: ${model3}; Colour: ${colour3}; Registration: ${reg3}`);

// Using rest
const [make4, ...rest] = getVehicle();
console.log(`Make: ${make4}, Rest: ${rest}`);

// Use array destructuring to swap values
let [value1, value2] = [1, 2];
console.log(`value1 = ${value1}, value2 = ${value2}`);
[value1, value2] = [value2, value1];
console.log(`value1 = ${value1}, value2 = ${value2}`);

// Use array destructuring to extract values from a parameter list
const printFirstAndLast = function([first,, last]) {
    console.log(`First: ${first}; Last: ${last}`);
}
printFirstAndLast(['Cats', 'Dogs', 'Mice']);

// Object destructuring
const { name: personFirstName, age: personAge} = { 
    name: 'Sam', 
    age: 20, 
    height: 170 
};

console.log(`Name: ${personFirstName}, Age: ${personAge}`);

// Extracting variables with the same name
const { carModel } = { carMake: "Hyundai", carModel: "i30" };
console.log(`Model: ${carModel}`);

// Object destructuring in a function's parameters
const printInfo = function({name: theName, age: theAge}) {
    console.log(`Name: ${theName}; Age: ${theAge}`);
};
const samantha = { name: 'Samantha', age: 20, height: 170 };
printInfo(samantha);

// Extracting with the spread operator
// Can be used to add to an object or to change properties
const addAge = function(person, age) {
    // Change 'last' and add 'age'
    return { ...person, last: person.last.toUpperCase(), age };
};

const parker = { 
    first: "Peter", 
    last: "Parker", 
    email: "spiderman@superheroes.com" 
};
console.log(addAge(parker, 15));
