// Spread operator works with function calls
const names = ['Laurel', 'Hardy']
const sayHello = function(name1, name2) {
    console.log('Hello ' + name1 + ' and ' + name2);
};
sayHello(...names);

// Spread operator can be used to copy, concatenate and manipulate arrays
const names1 = ['Tom', 'Jerry']
const names2 = ['Butch', 'Spike', 'Tyke'];
console.log([...names1, 'Brooke']);
console.log([...names1, ...names2]);
console.log([...names1, 'Meathead', ...names2]);

// Spread operator can be used to copy the contents of an object whilst also providing 
// new values for some fields or adding new fields
const sam = { name: 'Sam', age: 2};
console.log(sam);
console.log({...sam, age: 3});  // change a value
console.log({...sam, age: 4, height: 100});  // change a value and add a field
console.log(sam);  // show original to demonstrate that it hasn't changed