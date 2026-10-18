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

    const delaunay = d3.Delaunay.from(
        dataset,
        d => xScale(xAccessor(d)),
        d => yScale(yAccessor(d)),
    );

    const voronoi = delaunay.voronoi();
    voronoi.xmax = dimensions.boundedWidth;
    voronoi.ymax = dimensions.boundedHeight;

    bounds.selectAll(".voronoi")
        .data(dataset)
        .enter().append("path")
            .attr("class", "voronoi")
            .attr("d", (d,i) => voronoi.renderCell(i))
            // .attr("stroke", "salmon")
            .attr("fill", "transparent")
            .on("mouseenter", onMouseEnter)
            .on("mouseleave", onMouseLeave);            

    const tooltip = d3.select("#tooltip");
    function onMouseEnter(event) {
        
        const datum = d3.select(this).datum();

        // Add a dot to show the selected dot
        const dayDot = bounds.append("circle")
            .attr("class", "tooltipDot")
            .attr("cx", xScale(xAccessor(datum)))
            .attr("cy", yScale(yAccessor(datum)))
            .attr("r", 7)
            .style("fill", "maroon")
            .style("pointer-events", "none");

        // Format and set the data in the tooltip
        const formatHumidity = d3.format(".2f");
        tooltip.select("#humidity").text(formatHumidity(yAccessor(datum)));

        const formatDewPoint = d3.format(".2f");
        tooltip.select("#dew-point").text(formatDewPoint(xAccessor(datum)));

        const dateParser = d3.timeParse("%Y-%m-%d");
        const dateFormatter = d3.timeFormat("%A %-d %B %Y")
        tooltip.select("#date").text(dateFormatter(dateParser(datum.date)));
        
        // Set the x,y position of the tooltip and show it
        const x = xScale(xAccessor(datum)) + dimensions.margin.left;
        const y = yScale(yAccessor(datum)) + dimensions.margin.right;
        tooltip.style("transform", `translate(calc(-50% + ${x}px), calc(-100% + ${y}px))`);
        tooltip.style("opacity", 1);
    }

    function onMouseLeave(event) {
        // Remove the highlighted dot
        d3.selectAll(".tooltipDot")
            .remove();
        
        // Make the tooltip disappear
        tooltip.style("opacity", 0);
    }
}

drawScatterplot();