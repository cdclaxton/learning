const width = window.innerWidth * 0.9;
const height = 150;
const leftMargin = 10;
const topMargin = 10;

const rectWidth = 100;
const rectHeight = 100;

const nButtons = 4;

const createRectDataset = () => {
    return Array(nButtons).fill(0).map((_,i) => i)
}

// Add an SVG to the page
const wrapper = d3.select("#wrapper")
    .append("svg")
        .attr("width", width)
        .attr("height", height);

wrapper.append("g")
    .attr("class", "boxes")

const drawRects = (dataset) => {

    // console.log(dataset)

    // Transitions
    const exitTransition = d3.transition().duration(600);
    const updateTransition = exitTransition.transition().duration(600);    

    const boxes = wrapper.select(".boxes")
        .selectAll(".box")
        .data(dataset, d => d);

    boxes.exit()
        .transition(exitTransition)
            .attr("class", "box-leaving")
            .attr("height", 0)
            .remove();

    const newBoxes = boxes.enter()
        .append("rect")
            .attr("x", (d) => {
                console.log(d)
                return leftMargin + d*(leftMargin + rectWidth)
            })
            .attr("y", topMargin)
            .attr("height", rectHeight)
            .attr("width", rectWidth)
            .attr("class", "box-entering");

    newBoxes.merge(boxes)
        .transition(updateTransition)
            .attr("class", "box")
};

// Initialise the dataset and draw the rects
const dataset = createRectDataset(nButtons);
drawRects(dataset);

const toggleDatasetElement = (index) => {
    if (dataset.includes(index)) {
        const arrayIdx = dataset.indexOf(index);
        dataset.splice(arrayIdx, 1);
    } else {
        dataset.push(index);
    }
    drawRects(dataset)
};

// Define the buttons and add event listeners to mutate the data
for (let i=0; i<nButtons; i++) {
    const button = d3.select("body")
        .append("button")
            .text(`Toggle ${i}`);

    button.node().addEventListener("click", () => {
        toggleDatasetElement(i);
    });
}

