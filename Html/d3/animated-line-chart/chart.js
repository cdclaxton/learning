const generateValue = (previousValue) => {
    const range = 0.3
    return (Math.random() * range) - (range/2) + previousValue;
}

const dateFormat = "%Y-%m-%d"
const dateParser = d3.timeParse(dateFormat);

const createNewDataPoint = (previous) => {
    const previousDate = dateParser(previous.date);
    const previousValue = previous.value;

    const nextDay = d3.timeDay.offset(previousDate, 1);

    return {
        date: d3.timeFormat(dateFormat)(nextDay),
        value: generateValue(previousValue),
    }
}

const createInitialDataset = (nPoints) => {

    const result = [];

    // Get the current date
    const currentDate = new Date();
    const formattedCurrentDate = currentDate.toISOString().slice(0, 10);

    // Add the first data element
    result.push({
        date: formattedCurrentDate,
        value: generateValue(10),
    })

    for (let i=1; i<nPoints; i++) {
        const previous = result[result.length - 1];
        result.push(createNewDataPoint(previous));
    }

    return result;
}

// Data accessors
const xAccessor = d => dateParser(d.date);
const yAccessor = d => d.value;

// Define the chart dimensions
const dimensions = {
    width: window.innerWidth * 0.9,
    height: 400,
    margin: {
        top: 15,
        right: 15,
        bottom: 40,
        left: 60,
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


// Define the clip path to hide data as it's being rendered in the animation
bounds.append("defs")
    .append("clipPath")
        .attr("id", "bounds-clip-path")
    .append("rect")
        .attr("width", dimensions.boundedWidth)
        .attr("height", dimensions.boundedHeight);

const clip = bounds.append("g")
    .attr("clip-path", "url(#bounds-clip-path)")
    .append("path").attr("class", "line");

bounds.append("g")
    .attr("class", "line")

bounds.append("g")
    .attr("class", "x-axis")
    .style("transform", `translateY(${dimensions.boundedHeight}px)`);

bounds.append("g")
    .attr("class", "y-axis");

const drawLine = (dataset) => {

    // Create the scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(dataset, xAccessor))
        .range([0, dimensions.boundedWidth]);
    
    const yScale = d3.scaleLinear()
        .domain(d3.extent(dataset, yAccessor))
        .range([dimensions.boundedHeight, 0])
        .nice();

    // Draw the data
    const lineGenerator = d3.line()
        .x(d => xScale(xAccessor(d)))
        .y(d => yScale(yAccessor(d)));

    const lastTwoPoints = dataset.slice(-2);
    const pixelsBetweenLastPoints = xScale(xAccessor(lastTwoPoints[1])) - xScale(xAccessor(lastTwoPoints[0])); 

    const line = bounds.select(".line")
        .attr("d", lineGenerator(dataset))
        .style("transform", `translateX(${pixelsBetweenLastPoints}px)`)
        .transition().duration(1000)
            .style("transform", "none");

    // Draw the x-axis
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale);
    
    const xAxis = bounds.select(".x-axis")
        .transition().duration(1000)
        .call(xAxisGenerator);

    // Draw the y-axis
    const yAxisGenerator = d3.axisLeft()
        .scale(yScale);

    const yAxis = bounds.select(".y-axis")
        .call(yAxisGenerator);
};

// Generate the initial samples
let dataset = createInitialDataset(100);

// Update the data every 2 seconds
setInterval(() => {

    // Add a new sample
    dataset = [
        ...dataset.slice(1),
        createNewDataPoint(dataset[dataset.length - 1]),
    ];

    // Redraw the graph
    drawLine(dataset);

}, 2000);