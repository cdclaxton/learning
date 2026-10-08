async function drawBarChart(metric) {

    // Load the dataset
    const dataset = await d3.json("../weather_data.json");

    // Data accessor
    const metricAccessor = d => d[metric];
    
    const width = 600;
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

    // Create the bounds
    const bounds = wrapper.append("g")
        .style("transform", `translate(${dimensions.margin.left}px, ${dimensions.margin.top}px)`);
 
    // Create the scales
    const xScale = d3.scaleLinear()
        .domain(d3.extent(dataset, metricAccessor))
        .range([0, dimensions.boundedWidth])
        .nice();

    // Create the bins
    const binsGenerator = d3.histogram()
        .domain(xScale.domain())
        .value(metricAccessor)
        .thresholds(12);
    
    const bins = binsGenerator(dataset);
    
    // y-scale accessor
    const yAccessor = d => d.length;  // number of elements in array in the bin

    // y-scale
    const yScale = d3.scaleLinear()
        .domain([0, d3.max(bins, yAccessor)])
        .range([dimensions.boundedHeight, 0])
        .nice();

    // Group for the bins
    const binGroups = bounds.selectAll("g")
        .data(bins)
        .enter().append("g");

    const barPadding = 1;

    const barRects = binGroups.append("rect")
        .attr("x", d => xScale(d.x0) + barPadding/2)
        .attr("y", d => yScale(yAccessor(d)))
        .attr("width", d => d3.max([0, xScale(d.x1) - xScale(d.x0) - barPadding]))
        .attr("height", d => dimensions.boundedHeight - yScale(yAccessor(d)))
        .attr("fill", "cornflowerblue");

    // Add the labels
    binGroups.filter(yAccessor)
        .append("text")
            .attr("x", d => (xScale(d.x0) + xScale(d.x1))/2)
            .attr("y", d => yScale(yAccessor(d)) - 5)
            .text(yAccessor)
            .style("text-anchor", "middle")
            .attr("fill", "darkgrey")
            .style("font-size", "12px")
            .style("font-family", "sans-serif");

    // Calculate the mean of the dataset
    const mean = d3.mean(dataset, metricAccessor);

    // Add a line to show the mean
    bounds.append("line")
        .attr("x1", xScale(mean))
        .attr("y1", -15)
        .attr("x2", xScale(mean))
        .attr("y2", dimensions.boundedHeight)
        .attr("stroke", "maroon")
        .attr("stroke-dasharray", "2px 4px");

    bounds.append("text")
        .attr("x", xScale(mean))
        .attr("y", -20)
        .text("mean")
        .style("text-anchor", "middle")
        .attr("fill", "maroon")
        .style("font-size", "12px")
        .style("font-family", "sans-serif");

    // Draw the x-axis
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale);

    const xAxis = bounds.append("g")
        .call(xAxisGenerator)
            .style("transform", `translateY(${dimensions.boundedHeight}px)`);
    
    xAxis.append("text")
        .attr("x", dimensions.boundedWidth/2)
        .attr("y", dimensions.margin.bottom - 10)
        .text(metric)
        .style("text-transform", "capitalize")
        .style("text-anchor", "middle")
        .attr("fill", "black")
        .style("font-size", "12px")
        .style("font-family", "sans-serif");        
}

const metrics = [
    "windSpeed",
    "moonPhase",
    "dewPoint",
    "humidity",
    "uvIndex",
    "windBearing",
    "temperatureMin",
    "temperatureMax",
    "visibility",
    "cloudCover",
]

metrics.forEach(metric => drawBarChart(metric));
