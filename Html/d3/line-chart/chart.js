async function drawLineChart() {

    // Load the dataset
    const dataset = await d3.json("../weather_data.json");

    // Data accessors
    const yAccessor = d => d.temperatureMax;
    const dateParser = d3.timeParse("%Y-%m-%d");
    const xAccessor = d => dateParser(d.date);

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
    dimensions.boundedWidth = dimensions.width - dimensions.margin.left -
        dimensions.margin.right;
    dimensions.boundedHeight = dimensions.height - dimensions.margin.top - 
        dimensions.margin.bottom;

    // Get the div to append to and create the SVG
    const wrapper = d3.select("#wrapper")
        .append('svg')  // Add a new SVG element
        .attr("width", dimensions.width)
        .attr("height", dimensions.height);
 
    // Create a new group and apply a transformation
    const bounds = wrapper.append("g")
        .style("transform", `translate(${dimensions.margin.left}px, ${dimensions.margin.top}px)`);
    
    // Create the scales
    const yScale = d3.scaleLinear()
        .domain(d3.extent(dataset, yAccessor))
        .range([dimensions.boundedHeight, 0]);

    const xScale = d3.scaleTime()
        .domain(d3.extent(dataset, xAccessor))
        .range([0, dimensions.boundedWidth]);

    // Draw a box showing freezing temperatures (0 C, 32 F)
    const freezingTempYValue = yScale(32);
    bounds.append("rect")
        .attr("x", 0)
        .attr("y", freezingTempYValue)
        .attr("width", dimensions.boundedWidth)
        .attr("height", dimensions.boundedHeight - freezingTempYValue)
        .attr("fill", "#e0f3f3");

    const lineGenerator = d3.line()
        .x(d => xScale(xAccessor(d)))
        .y(d => yScale(yAccessor(d)));
    
    // Draw the line showing the temperatures
    bounds.append("path")
        .attr("d", lineGenerator(dataset))
        .attr("fill", "none")
        .attr("stroke", "#af9358")
        .attr("stroke-width", 2);
    
    // Add the y-axis
    const yAxisGenerator = d3.axisLeft()
        .scale(yScale);
    bounds.append("g")
        .call(yAxisGenerator);

    // Add the x-axis
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale);
    bounds.append("g")
        .call(xAxisGenerator)
        .style("transform", `translateY(${dimensions.boundedHeight}px)`);
}

drawLineChart();