async function drawLineChart() {

    // Load the dataset
    const data = await d3.json("../weather_data.json");
    const dataset = data.slice(0, 100);

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
            left: 50,
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
    const yAxis = bounds.append("g")
        .attr("class", "y-axis")
        .call(yAxisGenerator);
    
    const yAxisLabel = yAxis.append("text")
        .attr("class", "y-axis-label")
        .attr("x", -dimensions.boundedHeight/2)
        .attr("y", -dimensions.margin.left + 10)
        .html("Maximum temperature")

    // Add the x-axis
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale);
    bounds.append("g")
        .call(xAxisGenerator)
        .style("transform", `translateY(${dimensions.boundedHeight}px)`);

    const tooltip = d3.select("#tooltip");

    // Circle to highlight the closest point to the mouse pointer
    const tooltipCircle = bounds.append("circle")
        .attr("r", 4)
        .attr("stroke", "#af9358")
        .attr("fill", "white")
        .attr("stroke-width", 2)
        .style("opacity", 0);

    function onMouseMove(event) {
        const mousePosition = d3.pointer(event);
        const hoveredDate = xScale.invert(mousePosition[0])

        // Find the closest data index to the mouse
        const getDistanceFromDate = d => {
            return Math.abs(xAccessor(d) - hoveredDate)
        }
        const closestIndex = d3.scan(dataset, (a, b) => (
            getDistanceFromDate(a) - getDistanceFromDate(b)
        ));
        const closestDataPoint = dataset[closestIndex];

        const closestXValue = xAccessor(closestDataPoint);
        const closestYValue = yAccessor(closestDataPoint);

        // Set the date in the tooltip
        const dateFormatter = d3.timeFormat("%A %-d %B %Y")
        tooltip.select("#date").text(dateFormatter(closestXValue));

        // Set the temperature in the tooltip
        const temperatureFormatter = d => `${d3.format(".1f")(d)} F`;
        tooltip.select("#temperature").text(temperatureFormatter(closestYValue));

        // Position and make the tooltip visible
        const x = xScale(closestXValue) + dimensions.margin.left;
        const y = yScale(closestYValue) + dimensions.margin.top;      
        tooltip
            .style("transform", `translate(calc(-50% + ${x}px), calc(-100%  + ${y}px))`)
            .style("opacity", 1);

        // Position the circle to show the closest point to the mouse pointer
        tooltipCircle
            .attr("cx", xScale(closestXValue))
            .attr("cy", yScale(closestYValue))
            .style("opacity", 1);
    }

    function onMouseLeave() {
        tooltip.style("opacity", 0);
        tooltipCircle.style("opacity", 0);
    }

    // Add a rectangle in which to listen for mouse events
    const listeningRect = bounds.append("rect")
        .attr("class", "listening-rect")
        .attr("width", dimensions.boundedWidth)
        .attr("height", dimensions.boundedHeight)
        .on("mousemove", onMouseMove)
        .on("mouseleave", onMouseLeave);
}

drawLineChart();