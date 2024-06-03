const p1 = new Promise((resolve, reject) => {
    x = Math.random();
    if (x < 0.5) {
        resolve("Resolved");
    } else {
        reject("Rejected");
    }
})

p1.then((value) => {
    console.log(`${value} received`);
}).catch((value) => {
    console.log(`${value} caught`);
})


const p2 = new Promise((resolve, reject) => {
    resolve("p2 resolved");
})

const p3 = new Promise((resolve, reject) => {
    resolve("p3 resolved");
})

// Multiple promises, all required
Promise.all([p2, p3]).then((v1, v2) => {
    console.log(`Promise 1: ${v1}, Promise 2: ${v2}`);
});

// Multiple promises, but just one required
Promise.race([p1, p2]).then((value) => {
    console.log(`Race: ${value}`);
});