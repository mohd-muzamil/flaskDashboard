function glyph_test(chart, participant, sensor) {
    if (sensor == "acc") {
        pathColor = "red";
        datapath = "../../data/accelerometer_d3";
        attr = "acc";
    } else if (sensor == "gyr") {
        pathColor = "blue";
        datapath = "../../data/gyroscope_d3";
        attr = "gyr";
    } else if (sensor == "brt") {
        pathColor = "green";
        datapath = "../../data/brightness_d3";
        attr = "brt";
    } else if (sensor == "lck") {
        pathColor = "purple";
        datapath = "../../data/lockstate_d3";
        attr = "lck";
    }

    const config = {
        opacity: 0.8,
        strokewidth: 1
    }

    var radians = 0.0174532925,
        hourLabelYOffset = 7;

    // Set the dimensions of the canvas / graph
    var margin = { top: 25, right: 25, bottom: 25, left: 25 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
    // Parse the date / time
    var parseDate = d3.timeFormat("%Y-%b-%d");

    var arcGenerator = d3.arc();

    // Select the svg
    var svg = d3.select("#" + chart)
        .attr("width", width)
        .attr("height", height)
        .append('g')
        .attr("transform", `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom) / 2})`);

    var postForm = { //Fetch form data
        'filename': filename, //Store name fields value
        'participantId': participantId //Store name fields value
    };
        
    d3.csv("/filterParticipants")
    .header("Content-Type", "application/json")
    .post(JSON.stringify(postForm),
        function(data) {
        data = data.filter(function(row, i) {
            return row['participant'] == participant;
            })

    data.forEach(function(d) {
        // d.date = parseDate(d.date);
        d.minuteOfTheDay = +d.minuteOfTheDay;
        d[attr] = +d[attr];
    });

    var attrMinMax = d3.extent(data, function(d) { return d[attr]; });
    console.log("attrMinMax", attrMinMax)
    dates = Array.from(new Set(data.map(x => x.date)).values()).sort();
    d2i = {};
    dates.forEach((d, i) => d2i[d] = i);
    numDates = Object.keys(dates).length
    var find_radius = d3.scaleLinear()
        // .domain(d3.extent(data, function(d) { return + (new Date(...d.date.split("-").map((x)=>(+x)))); }))
        .domain([0, numDates])
        .rangeRound([Math.min(height, width) / 2 / numDates, Math.min(height, width) / 2]);

    var hourScale = d3.scaleLinear()
        .domain([0, 24])
        .range([0, 360]);


    slicePerAngle = (2 * Math.PI) / 1440;
    slices = data.map((d, i) => {
        if (d[attr] > 0) {
            const myPath = arcGenerator({
                    startAngle: d.minuteOfTheDay * slicePerAngle,
                    endAngle: (d.minuteOfTheDay + 1) * slicePerAngle,
                    innerRadius: find_radius(d2i[d.date]),
                    outerRadius: find_radius(d2i[d.date]) + (1 * find_radius(d2i[d.date] + 1) - find_radius(d2i[d.date])) //+ (1 * (find_radius(d2i[d.date] + 1) - find_radius(d2i[d.date])) * (d[attr] / attrMinMax[1]))
                })
                // Add the line
            svg.append("path")
                .datum(data)
                .attr("fill", pathColor)
                .attr("opacity", config.opacity)
                .attr("stroke", "black")
                .attr("stroke-width", 1 / 10)
                .attr("d", myPath)
        };
    })

    svg.append("path")


    // Creating a grid for reference
    radius = Math.min(width, height) / 2 + 15;

    // var grad = svg.append("defs")
    //     .append("linearGradient").attr("id", "grad")
    //     .attr("x1", "0%").attr("x2", "0%").attr("y1", "100%").attr("y2", "0%");

    // grad.append("stop").attr("offset", "50%").style("stop-color", "lightblue");
    // grad.append("stop").attr("offset", "50%").style("stop-color", "white");


    svg.selectAll(".gridCircles")
        .data(d3.range(0, numDates + 1, 1))
        .enter()
        .append("circle")
        .attr("class", "griCircles")
        .attr("fill", "none")
        // .style("fill", "url(#grad)")
        .attr("stroke", "black")
        .attr("opacity", 1)
        .attr("stroke-width", 1 / 5)
        .attr("r", function(d) {
            return find_radius(d)
        })

    svg.selectAll(".gridlines")
        .data(d3.range(0, 24, 1))
        .enter()
        .append("line")
        .attr("class", 'gridlines')
        .attr("x1", find_radius(0))
        .attr("x2", find_radius(numDates))
        .attr("opacity", 1)
        .attr("stroke", "black")
        .attr("stroke-width", 1 / 5)
        .attr("transform", function(d) { return `rotate(${hourScale(d)})` });

    svg.selectAll('.hourLabel')
        .data(d3.range(0, 24, 1))
        .enter()
        .append('text')
        .attr('class', 'hourLabel')
        .attr('text-anchor', 'middle')
        .style('font-size', '0.8em')
        .attr('x', function(d) {
            return radius * Math.sin(hourScale(d) * radians);
        })
        .attr('y', function(d) {
            return -radius * Math.cos(hourScale(d) * radians) + 7;
        })
        .text(function(d) {
            return d + "hr";
        });


    svg.selectAll('.dayLabel')
        .data(d3.range(0, numDates, 1))
        .enter()
        .append('text')
        .attr('class', 'dayLabel')
        .attr('text-anchor', 'middle')
        .style('font-size', '0.6em')
        .attr('x', 0)
        .attr('y', function(d) {
            return find_radius(d + 1);
        })
        .text(function(d) {
            return d;
        })
        .on('mouseover', function(d) {
            d3.select(this)
                .style('font-size', '1.6em')
                .style("cursor", "default")
        })
        .on('mouseout', function(d) {
            d3.select(this)
                .style('font-size', '0.6em')
                .style("fill", "black");
        });
    })
}

function createGrid(chart) {
    // Set the dimensions of the canvas / graph
    var margin = { top: 25, right: 25, bottom: 25, left: 25 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

    // Select the svg
    var svg = d3.select("#" + chart)
        .attr("width", width)
        .attr("height", height)
        .append('g')
        .attr("transform", `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom) / 2})`);

}

function updateglyph_test(chart, participant) {
    // ["acc", "gyr", "brt", "lck"]
    d3.select("#" + chart).selectAll('g').remove();
    // glyph_test(chart, participant, "acc")
    glyph_test(chart, participant, "gyr")
        // glyph_test(chart, participant, sensor = "brt")

}