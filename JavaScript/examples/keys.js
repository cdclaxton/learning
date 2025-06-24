const obj = {
    "example": 10,
    "another": "a string"
}

// [ 'example', 'another' ]
console.log(Object.keys(obj));

// [ 'another' ]
const matchingKeys = Object.keys(obj).filter(name => name.endsWith("er"));
console.log(matchingKeys);
console.log(matchingKeys.length);