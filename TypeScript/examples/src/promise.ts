async function getNumber(): Promise<number> {
    return 26;
}

getNumber().then(value => console.log(value));