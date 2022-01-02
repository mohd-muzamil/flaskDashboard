function glyph(chart) {
    console.log(chart)
    opacity = 0.8;
    strokewidth = 1;

    // Set the dimensions of the canvas / graph

    var svg = d3.select("#" + chart).selectAll("g").remove();

    // Set the dimensions of the canvas / graph
    var margin = { top: 10, right: 10, bottom: 10, left: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

    // Parse the date / time
    // var parseDate = d3.time.format("%d-%b-%y").parse;
    var parseDate = d3.timeFormat("%Y-%b-%d");
    // var formatTime = d3.time.format("%e %B");

    // Set the ranges
    num_days = 1.5
    var x = d3.scaleLinear().range([0, width / num_days]);
    var y = d3.scaleLinear().range([height / num_days, 0]);

    // Define the axes
    var yAxis = d3.axisLeft(y);
    var xAxis = d3.axisBottom(x);

    // Define the line
    // var lineGenerator = d3.line()
    //     .x(function (d) { return x(d.minuteOfTheDay); })
    //     .y(function (d) { return y(d.gyro); })
    //     .curve(d3.curveCardinal);

    // Define the div for the tooltip
    var div = d3.select("#" + chart).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);


    // Brightness data  Color:Green
    // Get the data
    d3.csv("../../data/brightness_d3", function(error, data) {
        console.log("brightness data", data)
        data = data.filter(function(row) {
            return row['participant'] == 'PROSITC0007'
        })
        data.forEach(function(d) {
            // d.date = parseDate(d.date);
            d.minuteOfTheDay = +d.minuteOfTheDay;
            d.brightnessLevel = +d.brightnessLevel;
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.minuteOfTheDay; }));
        y.domain([0, d3.max(data, function(d) { return d.brightnessLevel; })]);

        // Add the valueline path.
        // svg.selectAll("path")
        //     .data(data)
        //     .enter()
        //     .append("path")
        //     .attr("class", "line")
        //     // .attr("d", lineGenerator(data))
        //     .attr("stroke", "green")
        //     .attr("stroke-width", 2)
        //     .attr("fill", "none")
        // .on("mouseover", function (d) {
        //     div.transition()
        //         .duration(200)
        //         .style("opacity", .9);
        //     div.html(d.minuteOfTheDay + "<br/>" + d.brightnessLevel)
        //         .style("left", (d3.event.pageX) + "px")
        //         .style("top", (d3.event.pageY - 28) + "px");
        // })
        // .on("mouseout", function (d) {
        //     div.transition()
        //         .duration(500)
        //         .style("opacity", 0);
        // });

        // Add the area
        svg.append("path")
            .datum(data)
            .attr("fill", "#99d8c9") //green
            // .attr("fill", "none")    
            .attr("stroke", "#2ca25f")
            .attr("stroke-width", strokewidth)
            .style("opacity", opacity)
            .attr("d", d3.area()
                .x(function(d) { return x(d.minuteOfTheDay) })
                .y0(y(0))
                .y1(function(d) { return y(d.brightnessLevel) })
            )
            .attr("transform", `translate(0, ${0 * height / num_days})`)

        svg.append("g")
            .attr("class", "axis x")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "axis y")
            .call(yAxis);

    });

    // Accelerometer data   RED
    // Get the data
    d3.csv("../../data/accelerometer_d3", function(error, data) {
        data = data.filter(function(row) {
            return row['participant'] == 'PROSITC000234' && row['date'] == "2020-07-22";
        })
        data.forEach(function(d) {
            // d.date = parseDate(d.date);
            d.minuteOfTheDay = +d.minuteOfTheDay;
            d.acc = +d.acc;
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.minuteOfTheDay; }));
        y.domain([0, d3.max(data, function(d) { return d.acc; })]);

        // Add the area
        svg.append("path")
            .datum(data)
            .attr("fill", "#fc9272") //red
            // .attr("fill", "none")   
            .attr("stroke", "#de2d26")
            .attr("stroke-width", strokewidth)
            .style("opacity", opacity)
            .attr("d", d3.area()
                .x(function(d) { return x(d.minuteOfTheDay) })
                .y0(y(0))
                .y1(function(d) { return y(d.acc) })
            )
            .attr("transform", `translate(0, ${0.1 * height / num_days})`)
    });

    // Gyroscope data   BLUE
    // Get the data
    d3.csv("../../data/gyroscope_d3", function(error, data) {
        data = data.filter(function(row) {
            return row['participant'] == 'PROSITC000234' && row['date'] == "2020-07-22";
        })
        data.forEach(function(d) {
            // d.date = parseDate(d.date);
            d.minuteOfTheDay = +d.minuteOfTheDay;
            d.gyro = +d.gyro;
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.minuteOfTheDay; }));
        y.domain([0, d3.max(data, function(d) { return d.gyro; })]);

        // Add the area
        svg.append("path")
            .datum(data)
            .attr("fill", "#9ecae1") //blue
            // .attr("fill", "none")    //blue
            .attr("stroke", "#3182bd")
            .attr("stroke-width", strokewidth)
            .style("opacity", opacity)
            .attr("d", d3.area()
                .x(function(d) { return x(d.minuteOfTheDay) })
                .y0(y(0))
                .y1(function(d) { return y(d.gyro) })
            )
            .attr("transform", `translate(0, ${0.2 * height / num_days})`)
    });

}