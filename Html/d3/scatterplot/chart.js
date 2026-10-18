async function drawScatterplot() {

    // Load the dataset
    const dataset = await d3.json("../weather_data.json");
    
    // Accessors
    const xAccessor = d => d.dewPoint;
    const yAccessor = d => d.humidity;
    const colorAccessor = d => d.cloudCover;
    const sizeAccessor = d => d.temperatureHigh;

    const width = d3.min([
        window.innerWidth * 0.9,
        window.innerHeight * 0.9,
    ]);

    const dimensions = {
        width: width,
        height: width,
        margin: {
            top: 10,
            right: 10,
            bottom: 50,
            left: 50,
        }
    };

    dimensions.boundedWidth = dimensions.width -
        dimensions.margin.left - dimensions.margin.right;
    dimensions.boundedHeight = dimensions.height -
        dimensions.margin.top - dimensions.margin.bottom;

    // Add an SVG element to the page
    const wrapper = d3.select("#wrapper")
        .append("svg")
            .attr("width", dimensions.width)
            .attr("height", dimensions.height);
    
    // Create the bounds (part of the chart showing the data)
    const bounds = wrapper.append("g")
        .style("transform", `translate(${dimensions.margin.left}px, ${dimensions.margin.top}px)`);

    // Create the scales
    const xScale = d3.scaleLinear()
        .domain(d3.extent(dataset, xAccessor))
        .range([0, dimensions.boundedWidth])
        .nice();

    const yScale = d3.scaleLinear()
        .domain(d3.extent(dataset, yAccessor))
        .range([dimensions.boundedHeight, 0])
        .nice();

    const colourScale = d3.scaleLinear()
        .domain(d3.extent(dataset, colorAccessor))
        .range(["skyblue", "darkslategrey"]);

    const sizeScale = d3.scaleLinear()
        .domain(d3.extent(dataset, sizeAccessor))
        .range([2, 9]);
    
    // Add the data points
    const dots = bounds.selectAll("circle")
        .data(dataset)
        .enter()
        .append("circle")
            .attr("cx", d => xScale(xAccessor(d)))
            .attr("cy", d => yScale(yAccessor(d)))
            .attr("r", d => sizeScale(sizeAccessor(d)))
            .attr("fill", d => colourScale(colorAccessor(d)));

    // Draw the x-axis
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale);
    const xAxis = bounds.append("g")
        .call(xAxisGenerator)
        .style("transform", `translateY(${dimensions.boundedHeight}px)`)
    xAxis.append("text")
        .attr("x", dimensions.boundedWidth/2)
        .attr("y", dimensions.margin.bottom - 10)
        .attr("fill", "black")
        .style("font-size", "1.4em")
        .html("Dew point (&deg;F)");

    // Draw the y-axis
    const yAxisGenerator = d3.axisLeft()
        .scale(yScale)
        .ticks(4);
    const yAxis = bounds.append("g")
        .call(yAxisGenerator);
    yAxis.append("text")
        .attr("x", -dimensions.boundedHeight/2)  // NB x,y flipped due to rotation
        .attr("y", -dimensions.margin.left + 10)
        .attr("fill", "black")
        .style("font-size", "1.4em")
        .text("Relative humidity")
        .style("transform", "rotate(-90deg)")
        .style("text-anchor", "middle")

    // Add a legend
    const legendGroup = wrapper.append("g")
        .attr("transform", `translate(${dimensions.margin.left + 100}, 50)`)
    const legendTitle = legendGroup.append("text")
        .attr("y", -10)
        .text("Cloud cover")
        .attr("class", "legend-title")

    const defs = wrapper.append("defs");
    const legendGradientId = "legend-gradient";
    const gradient = defs.append("linearGradient")
        .attr("id", legendGradientId)
        .selectAll("stop")
            .data(colourScale.range())
            .enter().append("stop")
                .attr("stop-color", d => d)
                .attr("offset", (d,i) => `${i * 100}%`);

    const legendWidth = 120;
    const legendHeight = 16;
    const legendGradient = legendGroup.append("rect")
        .attr("x", -legendWidth/2)
        .attr("height", legendHeight)
        .attr("width", legendWidth)
        .style("fill", `url(#${legendGradientId})`);

    const legendValueRight = legendGroup.append("text")
        .attr("class", "legend-value")
        .attr("x", legendWidth/2 + 10)
        .attr("y", legendHeight/2)
        .attr("class", "legend-value")
        .text(colourScale.domain()[1])

    const legendValueLeft = legendGroup.append("text")
        .attr("class", "legend-value")
        .attr("x", -legendWidth/2 - 10)
        .attr("y", legendHeight/2)
        .attr("class", "legend-value")
        .text(colourScale.domain()[0])        
        .style("text-anchor", "end");
}

drawScatterplot();