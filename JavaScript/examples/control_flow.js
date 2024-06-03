// if ... else if ... else
let colour = "Blue";
if (colour === "Blue") {
    console.log("Blue is my favourite colour")
} else if (colour == "Green") {
    console.log("Green is also a good colour")
} else {
    console.log("I'm indifferent")
}

// switch statement
switch (2) {
    case 2:
        console.log("Number two");
        break;
    case 4:
        console.log("Number four");
        break;
    default:
        console.log("Not 2 or 4");
}

// Ternary (conditional) operator
// (condition) ? (if true) : (if false)
let r = 3 > 10 ? "first number larger" : "second number larger";
console.log(r);