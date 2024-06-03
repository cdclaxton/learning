const a = 3;
// a = 4; errors with TypeError: Assignment to constant variable.

// Object properties of a const object are not constant
const pedal = {brand: "Boss", "model": "DD-7", details: {"type": "delay"}};
console.log(pedal);  // { brand: 'Boss', model: 'DD-7', details: { type: 'delay' } }
pedal.brand = "Danelectro";
console.log(pedal);  // { brand: 'Danelectro', model: 'DD-7', details: { type: 'delay' } }

// Freeze top-level properties
Object.freeze(pedal); 
pedal.model = "Billion dollar boost";
console.log(pedal); // { brand: 'Danelectro', model: 'DD-7', details: { type: 'delay' } }

// Object.freeze() doesn't freeze lower-level properties
pedal.details.type = "boost";
console.log(pedal);  // { brand: 'Danelectro', model: 'DD-7', details: { type: 'boost' } }