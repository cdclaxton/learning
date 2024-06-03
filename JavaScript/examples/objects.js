// Define an object literal
// Properties are written as name:value pairs
let pedal = {make: "Boss", model: "DD-7"};
console.log(pedal); // { make: 'Boss', model: 'DD-7' }

// Access an object's properties
console.log(`Make: ${pedal.make}`); // Make: Boss
console.log(`Model: ${pedal['model']}`);  // Model: DD-7

// Objects can have methods (stored as properties in the function definition)
let reverb = {
    make: "Strymon",
    model: "BigSky",
    show: function() { 
        return "Make: " + this.make + ", model: " + this.model; 
    },
};
console.log(reverb.show()); // Make: Strymon, model: BigSky

// Can change and add new properties
reverb.model = "TimeLine";
reverb.price = 400;
console.log(`model: ${reverb.model}, price: ${reverb.price}`);

// Enhanced object literal
const createPerson = function(name, age, sport, sportFn) {
    return {
        name,
        age,
        toString() { return `${this.name} ${this.age}`; },
        [`play${sport}`] : sportFn
    };
}

const jamie = createPerson('Jamie', 21, 'Soccer', function() { console.log(`${this.name} kick!`); });
console.log(jamie.name);
console.log(jamie.toString());
jamie.playSoccer();