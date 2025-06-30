const data = [
    {
        id: "id-0",
        xMin: 0,
        xMax: 2,
    },
    {
        id: "id-1",
        xMin: 2,
        xMax: 4,
    },
    {
        id: "id-2",
        xMin: 4,
        xMax: 10,
    }
]

console.table(data);

const xValue = 2.5;
console.log(`xValue = ${xValue}`);

const filtered = data.filter(obj => obj.xMin < xValue && xValue < obj.xMax);
const idx = data.indexOf(filtered[0]);
console.log(data[idx]);
