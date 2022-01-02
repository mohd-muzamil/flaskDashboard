function glyph_test(chart, participant) {
    const config = {
        brtColor: "red",
        accColor: "green",
        gyrColor: "blue",
        lckColor: "purple",
        opacity: 0.8,
        strokewidth: 1
    }

    console.log("Chart2 participant: ", participant)

    // Set the dimensions of the canvas / graph
    var margin = { top: 20, right: 20, bottom: 20, left: 20 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
    // Parse the date / time
    var parseDate = d3.timeFormat("%Y-%b-%d");

    // Set the rangeskz

    // radiusScale = d3.scaleLinear().range([0, height / 2]);
    // colorScale = d3.scaleLinear();
    var arcGenerator = d3.arc();

    // Adds the svg canvas
    // var svg = d3.select("#mydiv").append("svg")
    var svg = d3.select("#" + chart)
        .attr("width", width)
        .attr("height", height)
        .append('g');

    d3.csv("../../data/accelerometer_d3", function(error, data) {
        data = data.filter(function(row) {
            return row['participant'] == participant //&& row['date'] <= "2020-07-23";// && row['date'] <= "2020-07-23";
        })

        data.forEach(function(d) {
            // d.date = parseDate(d.date);
            d.minuteOfTheDay = +d.minuteOfTheDay;
            d.acc = +d.acc;
            // console.log(d)
        });

        var accMinMax = d3.extent(data, function(d) { return d.acc; });

        // var find_radius = d3.scaleTime()
        //     .domain(d3.extent(data, function(d) { return d.date; }))
        //     .range([50, 200]);

        dates = Array.from(new Set(data.map(x => x.date)).values()).sort();
        d2i = {};
        dates.forEach((d, i) => d2i[d] = i);
        numDates = Object.keys(dates).length
        var find_radius = d3.scaleLinear()
            // .domain(d3.extent(data, function(d) { return + (new Date(...d.date.split("-").map((x)=>(+x)))); }))
            .domain([0, numDates])
            .rangeRound([Math.min(height, width) / 2 / numDates, Math.min(height, width) / 2]);

        var hourScale = d3.scaleLinear()
            .domain([0, 23])
            .range([0, 330]);

        // console.log(find_radius(data, function(d) { sreturn d.date; }))
        // data.map((d, i) =>{
        //     console.log("radius", find_radius(d.date))
        // });

        slicePerAngle = (2 * Math.PI) / 1440;
        slices = data.map((d, i) => {
                const my_path = arcGenerator({
                    startAngle: d.minuteOfTheDay * slicePerAngle,
                    endAngle: (d.minuteOfTheDay + 1) * slicePerAngle,
                    innerRadius: find_radius(d2i[d.date]),
                    outerRadius: find_radius(d2i[d.date]) + (d.acc / accMinMax[1] * 10) //find_radius(d.date)+(d.acc)+0.1
                });

                svg.append("path")
                    .attr("d", my_path)
                    .attr("fill", config.accColor)
                    .attr("transform", `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom) / 2})`)
                    // .style("stroke", "lightgreen")
                    // .style("stroke-width", "10px");


            })
            // // create circles using each radius.
        svg.selectAll("circle1")
            .data(data)
            .attr("class", "circle1")
            .enter().append("circle")
            .attr("fill", "none")
            .attr("stroke", "grey")
            .attr("opacity", 0.05)
            .attr("stroke-width", 1 / 10)
            .attr("r", function(d) {
                return find_radius(d2i[d.date])
            })
            .attr("transform", `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom) / 2})`);

        radius = (width + 2 * (margin.left + margin.right)) / 2;
        var ga = svg.append("g")
            .attr("class", "a axis")
            .selectAll("g")
            .data(d3.range(0, 24, 1))
            .enter().append("g")
            // .attr("transform", function (d) { return "rotate(" + -d + ")"; });
            .attr('transform', function(d) { return `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom) / 2})rotate(${-90 + d * 360 / 24})` }); // + 'rotate(' + function (d) { return d } + ')');


        ga.append("line")
            .attr("x1", find_radius(0))
            .attr("x2", find_radius(numDates - 1))
            .attr("opacity", 1)
            .attr("stroke", "grey")
            .attr("stroke-width", 1 / 10);

        ga.selectAll('.hour-label')
            .data(d3.range(1, 24, 1))
            .enter()
            .append('text')
            .attr('class', 'hour-label')
            .attr('text-anchor', 'middle')
            .attr('x', function(d) {
                return radius;
            })
            .attr('y', function(d) {
                return -radius;
            })
            .text(function(d) {
                return d[0];
            });

        // ga.selectAll('.hour-label')
        //     .data(d3.range(3, 13, 3))
        //     .enter()
        //     .append('text')
        //     .attr('class', 'hour-label')
        //     .attr('text-anchor', 'middle')
        //     .attr('x', function(d) {
        //         return hourLabelRadius * Math.sin(hourScale(d) * radians);
        //     })
        //     .attr('y', function(d) {
        //         return -hourLabelRadius * Math.cos(hourScale(d) * radians) + hourLabelYOffset;
        //     })
        //     .text(function(d) {
        //         return d;
        //     });

    })
}

function updateglyph_test(chart, participant) {
    d3.select("#" + chart).selectAll('g').remove();
    glyph_test(chart, participant)
}