// Create a new set
const fictional_names = new Set(['Jack', 'Jill', 'Dave', 'Jill']);
console.log(fictional_names);

// Number of elements in a set
console.log(`Number of elements: ${fictional_names.size}`);

// Add an element to the set
fictional_names.add('Mike');

// Does the set contain a value?
for (const name of ['Jack', 'Santa']) {
    console.log(`Set has ${name}: ${fictional_names.has(name)}`);
}

// Iterate over a Set using an enhanced for-loop
for (const name of fictional_names) {
    console.log(name);
}
// Set doesn't have methods like map() and filter()
console.log("Iterating through set and mapping:");
[...fictional_names]
    .filter(name => name.startsWith('J'))
    .map(name => name.toUpperCase())
    .forEach(name => console.log(name));