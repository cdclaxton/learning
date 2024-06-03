// For loop
const cats = ['Bill', 'Jeff', 'Pete', 'Biggles', 'Jasmin'];
let info = "My cats are called "
for (let i=0; i<cats.length; i++) {
    info += cats[i]
    if (i < cats.length-1) {
        info += ", "
    }
}
console.log(info)

// Break out of a loop -- example finding the square root of a number
let S = 125348;
let x = S / 2;

for (let i = 0; i < 20; i++) {
    let an = (S - x * x) / (2 * x);
    let bn = x + an;
    let xNew = bn - (an * an) / (2 * bn);

    let error = Math.abs(S - (xNew * xNew));
    if (error < 0.0001) {
        console.log("Found solution on " + i + "th iteration");
        break;
    }
    x = xNew;
}

console.log("sqrt(" + S + ") = " + Math.sqrt(S));
console.log("approx. solution to sqrt(" + S + ") = " + x);

// while loop
let reindeers = ["Dasher", "Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Donner", "Blitzen"];
let r = 0;
while (r < reindeers.length) {
    console.log("Reindeer " + r + " - " + reindeers[r]);
    r += 1;
}

// do ... while loop
let i2 = 1;
do {
    console.log(i2 + " * " + i2 + " = " + i2*i2);
    i2 += 1;
} while (i2 < 4);

// Enhanced for-loop
for (const i of reindeers) {
    console.log(i);
}

// Access the index using the entries() function
// Using array destructuring (with immutable variables for safety):
for (const [i, name] of reindeers.entries()) {
    console.log(i + " --> " + name);
}