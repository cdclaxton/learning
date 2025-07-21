function printId(id: number | string) {
    if (typeof id === "string") {
        console.log(`String ID: ${id.toUpperCase()}`);
    } else {
        console.log(`Number ID: ${id}`)
    }
}

printId(123);
printId("a123-cde");

function welcome(people: string | string[]) {
    if (Array.isArray(people)) {
        console.log(`Welcome everyone: ${people.join(' and ')}`);
    } else {
        console.log(`Welcome, ${people}`);
    }
}

welcome('Chris');
welcome(['Bob', 'Sandy']);