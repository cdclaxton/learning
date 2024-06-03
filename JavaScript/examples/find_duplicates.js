// Script to find duplicate edges in an array.

let edges = [
    {
        "src": "a",
        "dst": "b"
    },
    {
        "src": "b",
        "dst": "c"
    }, 
    {
        "src": "a",
        "dst": "b"
    },       
];

let s = new Set();

for (let edge of edges) {
    let key = edge.src + " " + edge.dst;
    if (s.has(key)) {
        console.log(`Found duplicate edge: ${edge.src} -> ${edge.dst}`);
    }
    s.add(key);
}
