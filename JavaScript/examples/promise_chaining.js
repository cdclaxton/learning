// -----------------------------------------------------------------------------
// Chaining functions that return a Promise
// -----------------------------------------------------------------------------

const buildRandomPromise = (pSucceed) => {
    return new Promise((resolve, reject) => {
        x = Math.random();
        if (x < pSucceed) {
            resolve(Math.random());
        } else {
            reject("Rejected in buildRandomPromise");
        }
    })
};

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

buildRandomPromise(0.7)
    .then(value => {
        console.log(`Resolve after buildRandomPromise(): ${value}`);
        return doubleValue(0.6, value);
    })
    .then(value => console.log(`Resolve after doubleValue(): ${value}`))
    .catch((err) => console.error(`Reject occurred: ${err}`))
    .finally(() => console.log('In finally'))