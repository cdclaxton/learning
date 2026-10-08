const generateDataset = () => {

    // Number of elements
    const minElements = 5;
    const maxElements = 8;
    const nElements = Math.round(Math.random() * (maxElements - minElements)) + minElements;

    const xStart = 0;
    const xSpacing = 2;
    const minY = 0;
    const maxY = 10;

    const result = [];

    for (let i=0; i<nElements; i++) {
        result.push({
            x: xStart + xSpacing * i,
            y: Math.random() * (maxY - minY) + minY,
            id: `${i}`,
        });
    }

    return result;
};

// Define the dimensions of the chart
const width = window.innerWidth * 0.9;
const dimensions = {
    width: width,
    height: width * 0.6,
    margin: {
        top: 30,
        right: 10,
        bottom: 50,
        left: 50,
    },
}
dimensions.boundedWidth = dimensions.width -
    dimensions.margin.left - dimensions.margin.right;
dimensions.boundedHeight = dimensions.height -
    dimensions.margin.top - dimensions.margin.bottom;

// Add the SVG to the page
const wrapper = d3.select("#wrapper")
    .append("svg")
        .attr("width", dimensions.width)
        .attr("height", dimensions.height);

// Create the bounds (chart data area)
const bounds = wrapper.append("g")
    .style("transform", `translate(${dimensions.margin.left}px, ${dimensions.margin.top}px)`);    

// Add the static parts to the bounds
bounds.append("g")
    .attr("class", "bars");
bounds.append("g")
    .attr("class", "x-axis")
    .style("transform", `translateY(${dimensions.boundedHeight}px)`)
    .append("text")
        .attr("class", "x-axis-label")
        .attr("x", dimensions.boundedWidth / 2)
        .attr("y", dimensions.margin.bottom - 10);

// Data accessors
const xAccessor = d => d.x;
const yAccessor = d => d.y;

const drawBarChart = (dataset) => {

    // Transitions
    const exitTransition = d3.transition().duration(600);
    const updateTransition = exitTransition.transition().duration(600);

    // Define the x- and y-scales
    const xSpacing = dataset[1].x - dataset[0].x;  // Assume constant spacing
    const barWidth = xSpacing / 1.5; 
    const xScale = d3.scaleLinear()
        .domain([dataset[0].x - barWidth/2, dataset[dataset.length - 1].x + barWidth/2])
        .range([0, dimensions.boundedWidth])

    const yScale = d3.scaleLinear()
        .domain(d3.extent(dataset, yAccessor))
        .range([dimensions.boundedHeight, 0])
        .nice();
    
    // Add the bars
    const barGroups = bounds.select(".bars")
        .selectAll(".bar")
        .data(dataset, d => d.id);

    // Remove the old bars
    const oldBarGroups = barGroups.exit();
    oldBarGroups.selectAll("rect")
        .style("fill", "red")
        .transition(exitTransition)
            .attr("y", dimensions.boundedHeight)
            .attr("height", 0)
    oldBarGroups.selectAll("text")
        .transition(exitTransition)
            .attr("y", dimensions.boundedHeight)
    oldBarGroups
        .transition(exitTransition)
        .remove();

    // Add the new bars
    const newBarGroups = barGroups.enter().append("g")
        .attr("class", "bar");

    newBarGroups.append("rect")
        .attr("x", d => xScale(xAccessor(d) - barWidth/2))
        .attr("y", d => dimensions.boundedHeight)
        .attr("height", 0)
        .attr("width", xScale(barWidth/2))
        .style("fill", "yellowgreen");

    newBarGroups.append("text")
        .attr("x", d => xScale(xAccessor(d) - barWidth/2))
        .attr("y", dimensions.boundedHeight)
        .style("text-anchor", "middle")
        .style("font-family", "sans-serif");

    // Set the new and updated bars
    const newAndUpdatedBarGroups = newBarGroups.merge(barGroups);

    const barRects = newAndUpdatedBarGroups.select("rect")
        .transition(updateTransition)
        .attr("x", d => xScale(xAccessor(d) - barWidth/2))
        .attr("y", d => yScale(yAccessor(d)))
        .attr("height", d => dimensions.boundedHeight - yScale(yAccessor(d)))
        .attr("width", xScale(barWidth/2))
        .style("fill", "cornflowerblue");        
    
    const barText = newAndUpdatedBarGroups.select("text")
        .transition(updateTransition)
            .attr("x", d => xScale(xAccessor(d)))
            .attr("y", d => yScale(yAccessor(d)) - 5)
            .text(d => yAccessor(d).toFixed(2))

    // Add the x-axis label
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale);
    const xAxis = bounds.select(".x-axis")
        .transition(updateTransition)
        .call(xAxisGenerator)            
}

// Generate a synthetic dataset and draw an initial bar chart
drawBarChart(generateDataset());

// Define the button to change the data
const button = d3.select("body")
    .append("button")
        .text("Update data");

const onClick = () => {
    drawBarChart(generateDataset());
}
button.node().addEventListener("click", onClick);
