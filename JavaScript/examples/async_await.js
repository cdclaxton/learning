// A function with 'async' before it always returns a Promise
async function f() {
    return 1;
}

f().then(v => console.log(v)); // 1

// 'await' makes JS wait until the Promose is settled
async function f2() {
    let p = new Promise((resolve, reject) => {
        setTimeout(() => resolve('resolved'), 100);
    });

    let result = await p;
    console.log(`result = ${result}`);
}

f2();

const doubleValue = (pSucceed, value) => {
    return new Promise((resolve, reject) => {
        x = Math.random();
        if (x < pSucceed) {
            resolve(2 * value);
        } else {
            reject("Rejected in doubleValue");
        }        
    });
};

async function f3() {
    try {
        const v1 = await doubleValue(0.6, 2.0);
        const v2 = await doubleValue(0.7, v1);
        console.log(`f3() succeeded: ${v2}`);
    } catch (err) {
        console.log(`f3() error: ${err}`);
    }
}

f3();