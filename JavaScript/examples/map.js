// Map
const pedals = new Map([
    ['Timeline', 'Delay'], 
    ['ModFactor', 'Modulation'], 
    ['TS-9', 'Overdrive']]);

// Add a key-value pair to the map
pedals.set('BigSky', 'Reverb');
console.log(pedals);

// Iterate over a map
for (const [name, tpe] of pedals.entries()) {
    console.log(`${name}: ${tpe}`);
}

// Iternal iterator -- note the odd order of the key and value
pedals.forEach((value, key) => console.log(`${key} -> ${value}`));

// Iterate just over the values
pedals.forEach(value => console.log(value));

// Has key?
console.log(pedals.has('Timeline'));