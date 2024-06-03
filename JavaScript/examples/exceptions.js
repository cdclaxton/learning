// Use throw <string or number> to throw an exception
const f = (x) => {
    if (x === 0) {
        throw "Zero passed to function"
    }
    return 10/x;
}

try {
    console.log(f(0));
} catch (err) {
    console.error(err);
} finally {
    console.log("In finally block");
}