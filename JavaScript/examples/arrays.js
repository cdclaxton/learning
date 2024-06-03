// Define an array
let pedals = ["Caline Tantrum", "Boss DD-7", "Boss RV-5"];
console.log(`Pedals: ${pedals}`);

// Arrays are mutable
pedals[0] = "Ibanez TS-9";
console.log(`Pedals: ${pedals}`);

// concat -- join arrays
let allPedals = pedals.concat(["Strymon BigSky"]);
console.log(`Pedals: ${allPedals}`);

// join
let joined = pedals.join("|");
console.log(joined); // Ibanez TS-9|Boss DD-7|Boss RV-5

// length
console.log(pedals.length);

// pop
let days = ["Monday", "Tuesday", "Wednesday"];
console.log(`Pop(): ${days.pop()}`); // Wednesday
console.log(`Days: ${days}`); // Days: Monday,Tuesday

// push
let colours = ["red", "blue", "green"];
colours.push("orange");
console.log(`Colours: ${colours}`); // Colours: red,blue,green,orange

// reverse
console.log(`Reversed: ${colours.reverse()}`);

// shift -- remove first element (like pop, but for the front)
colours = ["red", "blue", "green"];
console.log(`Shift: ${colours.shift()}`);
console.log(`Colours: ${colours}`);

// slice(begin, end) -- shallow copy of a portion of an array
// (end is not included)
let s = ['ant', 'bison', 'camel', 'duck', 'elephant'].slice(2,4);
console.log(`s: ${s}`); // camel,duck

// splice -- remove or replace existing elements in place
let m1 = ['Jan', 'March', 'April', 'June']
m1.splice(1, 0, "Feb");
console.log(`m1: ${m1}`); // Jan,Feb,March,April,June

let m2 = [0, 1, 2, 3];
m2.splice(2, 1, 20);
console.log(`m2: ${m2}`);  // 0,1,20,3

// sort in-place
colours = ["red", "blue", "green"];
colours.sort()
console.log(`colours: ${colours}`); // blue,green,red

// sort with a compare method
let x = [ '1', '111', '1111', '11' ];
x.sort((a,b) => {return a.length - b.length});
console.log(`x: ${x}`);  // 1,11,111,1111

// toString -- comma separated
console.log(`${x.toString()}`); // 1,11,111,1111

// unshift -- add element to start of array (returns new array length)
colours.unshift("violet");
console.log(`colours: ${colours}`); // violet,blue,green,red