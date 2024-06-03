// Parse a JSON string
s = '{"name":"Chris","age":39}';
console.log(JSON.parse(s).name);

// Convert JSON to a String
x = JSON.stringify({name: "Chris", age: 39, car: "Hyundai i30"})
console.log(x);