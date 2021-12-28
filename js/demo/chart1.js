function chart1() {
    // set the dimensions and margins of the graph
    const svg = d3.select('#chart1');
    var margin = { top: 50, right: 50, bottom: 50, left: 10 },
        width = $("#chart1").width() - margin.left - margin.right,
        height = $("#chart1").height() - margin.top - margin.bottom;

    // parse the date / time
    var parseTime = d3.timeParse("%d-%b-%y");

    // set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // define the line
    var valueline = d3.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.close); });

    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    svg
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Get the data
    d3.csv("../../data/demo/chart1Data.csv").then(function(data) {


        // format the data
        data.forEach(function(d) {
            d.date = parseTime(d.date);
            d.close = +d.close;
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) { return d.close; })]);

        // Add the valueline path.
        svg.append("path")
            .data([data])
            .attr("class", "line")
            .attr("d", valueline);

        // Add the scatterplot
        svg.selectAll("dot")
            .data(data)
            .enter().append("circle")
            .filter(function(d) { return d.close < 400 }) // <== This line
            .style("fill", "red") // <== and this one
            .attr("r", 5)
            .attr("cx", function(d) { return x(d.date); })
            .attr("cy", function(d) { return y(d.close); });

        // Add the X Axis
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // Add the Y Axis
        svg.append("g")
            .call(d3.axisLeft(y));

    });
}