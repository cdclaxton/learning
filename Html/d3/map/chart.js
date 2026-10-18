async function drawMap() {

    // Import country shapes
    const countryShapes = await d3.json("../world-geojson.json");

    const countryNameAccessor = d => d.properties["NAME"];
    const countryIdAccessor = d => d.properties["ADM0_A3_IS"];

    // Load the World Bank dataset
    const dataset = await d3.csv("../databank_data.csv");
    const metric = "Population growth (annual %)";

    // Create a summary of country-to-metric
    const metricByCountry = {};
    dataset.forEach(d => {
        if (d["Series Name"] === metric) {
            metricByCountry[d["Country Code"]] = +d["2023 [YR2023]"] || 0;
        }
    });

    // Chart dimensions
    const dimensions = {
        width: window.innerWidth * 0.9,
        margin: {
            top: 10,
            right: 10,
            bottom: 10,
            left: 10,
        },
    }
    dimensions.boundedWidth = dimensions.width - dimensions.margin.left - dimensions.margin.right;

    // Define a sphere
    const sphere = { type: "Sphere" };

    // Projection function
    const projection = d3.geoEqualEarth()
        .fitWidth(dimensions.boundedWidth, sphere);

    const pathGenerator = d3.geoPath(projection);
    const [[x0, y0], [x1, y1]] = pathGenerator.bounds(sphere);
    dimensions.boundedHeight = y1;
    dimensions.height = dimensions.boundedHeight + dimensions.margin.top + dimensions.margin.bottom;

    // Add the SVG
    const wrapper = d3.select("#wrapper")
        .append("svg")
        .attr("width", dimensions.width)
        .attr("height", dimensions.height);

    const bounds = wrapper.append("g")
        .style("transform", `translate(${dimensions.margin.left}px, ${dimensions.margin.top}px)`);

    // Create the metric scale
    const metricValues = Object.values(metricByCountry);
    const metricValueExtent = d3.extent(metricValues);
    const maxChange = d3.max([-metricValueExtent[0], metricValueExtent[1]])
    const colourScale = d3.scaleLinear()
        .domain([-maxChange, 0, maxChange])
        .range(["indigo", "white", "darkgreen"]);

    // Draw the earth outline
    const earth = bounds.append("path")
        .attr("class", "earth")
        .attr("d", pathGenerator(sphere))

    // Add a graticule
    const graticuleJson = d3.geoGraticule10();
    const graticule = bounds.append("path")
        .attr("class", "graticule")
        .attr("d", pathGenerator(graticuleJson));

    // Add the countries
    const countries = bounds.selectAll(".country")
        .data(countryShapes.features)
        .enter().append("path")
        .attr("class", "country")
        .attr("d", pathGenerator)
        .attr("fill", d => {
            const metricValue = metricByCountry[countryIdAccessor(d)]
            if (typeof (metricValue) === "undefined") {
                return "#e2e6e9"
            }
            return colourScale(metricValue)
        })

    // Add a legend
    const legendGroup = wrapper.append("g")
        .attr("transform", `translate(120, ${dimensions.width < 800 ? dimensions.boundedHeight - 30 : dimensions.boundedHeight * 0.5})`);
    const legendTitle = legendGroup.append("text")
        .attr("y", -23)
        .attr("class", "legend-title")
        .text("Population growth")

    const legendByline = legendGroup.append("text")
        .attr("y", -9)
        .attr("class", "legend-byline")
        .text("Percent change in 2023");

    const defs = wrapper.append("defs")
    const legendGradientId = "legend-gradient";
    const gradient = defs.append("linearGradient")
        .attr("id", legendGradientId)
        .selectAll("stop")
        .data(colourScale.range())
        .enter().append("stop")
        .attr("stop-color", d => d)
        .attr("offset", (d, i) => `${i * 100 / 2}%`);

    const legendWidth = 120;
    const legendHeight = 16;
    const legendGradient = legendGroup.append("rect")
        .attr("x", -legendWidth / 2)
        .attr("height", legendHeight)
        .attr("width", legendWidth)
        .style("fill", `url(#${legendGradientId})`);

    const legendValueRight = legendGroup.append("text")
        .attr("class", "legend-value")
        .attr("x", legendWidth/2 + 10)
        .attr("y", legendHeight/2)
        .text(`${d3.format(".1f")(maxChange)}%`);

    const legendValueLeft = legendGroup.append("text")
        .attr("class", "legend-value")
        .attr("x", -legendWidth/2 - 10)
        .attr("y", legendHeight/2)
        .text(`${d3.format(".1f")(-maxChange)}%`)
        .style("text-anchor", "end");

    // Get the user's current location
    navigator.geolocation.getCurrentPosition(myPosition => {
        const [x,y] = projection([myPosition.coords.longitude, myPosition.coords.latitude]);
        const myLocation = bounds.append("circle")
            .attr("class", "my-location")
            .attr("cx", x)
            .attr("cy", y)
            .attr("r", 0)
            .transition().duration(500)
            .attr("r", 5);
    })

    // Setup the interactions
    function onMouseEnter(event) {
        const datum = d3.select(this).datum();        
        const metricValue = metricByCountry[countryIdAccessor(datum)];

        // Find the centre of the country in pixels
        const [centreX, centreY] = pathGenerator.centroid(datum);
        const x = centreX + dimensions.margin.left;
        const y = centreY + dimensions.margin.top;

        tooltip.style("transform", `translate(calc(-50% + ${x}px), calc(-100% + ${y}px))`);

        tooltip.select("#country").text(countryNameAccessor(datum));
        tooltip.select("#value").text(`${d3.format(",.2f")(metricValue || 0)}%`);
        tooltip.style("opacity", 1);
    }

    function onMouseLeave() {
        tooltip.style("opacity", 0);
    }

    countries.on("mouseenter", onMouseEnter)
        .on("mouseleave", onMouseLeave);
    const tooltip = d3.select("#tooltip");
}

drawMap();