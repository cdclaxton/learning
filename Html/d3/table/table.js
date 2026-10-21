async function drawTable() {

    // Data accessors and formatters
    const dateParser = d3.timeParse("%Y-%m-%d");
    const dateAccessor = d => dateParser(d.date);
    const dateFormat = d => d3.timeFormat("%d/%m")(dateParser(d));
    const format24HourTime = d => +d3.timeFormat("%H")(new Date(d * 1000));

    // Load the data and sort by time
    const dataset = await d3.json("../weather_data.json");
    dataset.sort((a,b) => dateAccessor(a) - dateAccessor(b));

    // Number of rows of data to show
    const numberOfRows = 100;

    // Scales
    const colourScale = d3.interpolateHcl("#a5c3e8", "#efa8a1");
    const greyScale = d3.interpolateHcl("#fff", "#bdc4ca");
    const tempScale = d3.scaleLinear()
        .domain(d3.extent(dataset.slice(0, numberOfRows), d => d.temperatureMax))
        .range([0, 1]);
    const windScale = d3.scaleLinear()
        .domain(d3.extent(dataset.slice(0, numberOfRows), d => d.windSpeed))
        .range([0, 1]);
    const timeScale = d3.scaleLinear()
        .domain([0, 24]) // hours
        .range([0, 80]);  // percent
    
    // Columns to show
    const columns = [
        {
            label: "Day",
            type: "text",
            format: d => dateFormat(d.date),
        },
        {
            label: "Summary",
            type: "text",
            format: d => d.summary,
        },
        {
            label: "Max temp",
            type: "number",
            format: d => d3.format(".1f")(d.temperatureMax),
            background: d => colourScale(tempScale(d.temperatureMax)),
        },
        {
            label: "Max temp time",
            type: "marker",
            format: d => "|",
            transform: d => `translateX(${timeScale(format24HourTime(d.apparentTemperatureMaxTime))}%)`
        },
        {
            label: "Wind speed",
            type: "number",
            format: d => d3.format(".2f")(d.windSpeed),
            background: d => greyScale(windScale(d.windSpeed))
        },
        {
            label: "Precipitation",
            type: "centered",
            format: d => d.precipType === "snow" ? "❄" : d.precipType === "rain" ? "☂" : "",
        },
        {
            label: "UV index",
            type: "symbol",
            format: d => new Array(+d.uvIndex).fill("☀").join(""),
        }
    ]

    // Select the table in the HTML
    const table = d3.select("#table");

    // Create the table header
    table.append("thead").append("tr")
        .selectAll("thead")
        .data(columns)
        .enter().append("th")
            .text(d => d.label)
            .attr("class", d => d.type)
    
    const body = table.append("tbody");

    dataset.slice(0, numberOfRows).forEach(d => {
        body.append("tr")
            .selectAll("td")
            .data(columns)
            .enter().append("td")
                .text(column => column.format(d))
                .attr("class", column => column.type)
                .style("background", column => column.background && column.background(d))
                .style("transform", column => column.transform && column.transform(d))
    });
}

drawTable();