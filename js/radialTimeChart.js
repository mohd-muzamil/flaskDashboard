// This script is used to plot radial chart in second svg
function radialTime(chart, dependentChart1, selectedId, featureType, featurelist, classLabel, labels, attributes) {
        // var pathColor = {"brt": "#1b9e77", "acc": "#d95f02", "gyro": "#7570b3", "lck": "#a6bddb"}
        // var pathColor = {"brt": "#1f78b4", "acc": "#33a02c", "gyro": "#b2df8a", "lck": "#dadaeb"}    //darkBlue, darkgreen, lightgreen, lightpurple
        // var pathColor = {"brt": "#377eb8", "acc": "#e41a1c", "gyro": "#fb8072", "lck": "#d0d1e6"}    //darkBlue, darkRed, lightRed, lightBlue
        // var pathColor = {"brt": "#e41a1c", "acc": "#4daf4a", "gyro": "#b2df8a", "lck": "#d9d9d9"}    //darkRed, darkGreen, lightgreen, lightGray
    var pathColor = { "checkbox": "#F4F5F5", "acc": "#e41a1c", "gyro": "#377eb8", "brt": "#4daf4a", "lck": "#fdc086", "noise":"#984ea3" } //{"acc": "dred", "gyro": "dblue", "brt": "dgreen", "lck": "lyellow", "noise": "dpurple"}
    var dayColor = {0:"#f7f7f7", 1:"#d9d9d9", 2:"#bdbdbd", 3:"#969696", 4:"#737373", 5:"#525252", 6:"#252525"}
    var gridPlotted = true

    // Set the dimensions of the canvas / graph
    const margin = { left: 25, top: 5, right: 25, bottom: 25 },
    width = Math.floor(+$("#" + chart).width()),
    height = Math.floor(+$("#" + chart).height()),
    xHigh = (width - margin.left - margin.right),
    yHigh = (height - margin.top - margin.bottom)

    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style('font-size', '1em')
        .style("border-width", "2px")
        .style("padding", "5px")
        .style('background-color', 'white')
        .style('border-radius', '10% 10% 10% 10%')
    var deltaLegend = 1

    var postForm = { //Fetch form data
        // 'filename': filename, //Store name fields value
        'id': selectedId, //Store name fields value
        "attributes": attributes
    };

    //fetcing filtered id data from flask server
    d3.csv("/filterparticipantIdsNew")
        // d3.csv("/filterparticipantIds")
        .header("Content-Type", "application/json")
        .post(JSON.stringify(postForm),
            function(data) {
                data.forEach(function(d) {
                    d.minuteOfTheDay = +d.minuteOfTheDay;
                    d.brt = +d.brt;
                    d.acc = +d.acc;
                    d.gyro = +d.gyro;
                    d.lck = +d.lck;
                    d.noise = +d.noise
                });
                dates = Array.from(new Set(data.map(d => d.date)).values()).sort();
                d2i = {};
                dates.forEach((d, i) => d2i[d] = i + 1);
                numDates = Object.keys(dates).length

                var sliderMin = 1
                var sliderMax = numDates
                var starting_min = 1
                var starting_max = numDates

                attributesTemp = attributes
                delete attributesTemp["checkbox"]

                // plotRadier function here
                function plotRadial(starting_min, starting_max) {
                    const config = {
                        opacity: 0.8,
                        strokewidth: 1
                    }

                    const radians = 0.0174532925,
                        hourLabelYOffset = 2;

                    // Select the svg
                    var svg = d3.select("#" + chart)
                        .attr("width", xHigh)
                        .attr("height", yHigh)
                        .append('g')
                        .attr("transform", `translate(${margin.left + xHigh/2}, ${margin.top + yHigh/2})`);

                    var find_radius = d3.scaleLinear()
                        .domain([starting_min - 1, starting_max])
                        .range([Math.min(yHigh, xHigh) / 8, Math.min(yHigh, xHigh) / 2]);

                    var hourScale = d3.scaleLinear()
                        .domain([0, 24])
                        .range([0, 360]);

                    var x = d3.scaleLinear()
                        .domain([0, 1440])
                        .range([0, 2 * Math.PI]);

                    attributes = Object.assign({}, { "checkbox": true }, attributes)

                    for (let i = 0; i < Object.keys(attributes).length; i++) {
                        attr = Object.keys(attributes)[i]
                        if (attributes[attr]) {
                            for (let d = starting_min; d <= starting_max; d++) {
                                currDate = d;

                                if (attr == "checkbox") {
                                    if (d % 2 == 0) {
                                        datum = Array.from(Array(1440).keys())
                                        datum = datum.map(e => ({ "minuteOfTheDay": e, "checkbox": e % 60 == 0 ? 0 : 1 }))
                                    } else
                                        continue
                                    datum = Array.from(Array(1440).keys())
                                    datum = datum.map(e => ({ "minuteOfTheDay": e, "checkbox": e % 60 == 0 ? 0 : 1 }))
                                } else {
                                    datum = data.filter(function(row, i) {
                                        return d2i[row['date']] == currDate && row[attr] != NaN;
                                    })
                                }

                                y = d3.scaleLinear()
                                    .domain(d3.extent(datum, function(d) { return d[attr]; }))
                                    .range([find_radius(currDate - 1), find_radius(currDate)]);

                                const area = d3.areaRadial()
                                    .angle(d => x(+d.minuteOfTheDay))
                                    .innerRadius(d => y(0))
                                    .outerRadius(d => y(+d[attr]));

                                // Add the line
                                svg.append("g").append("path")
                                    .attr("class", "areaPath")
                                    .attr("fill", pathColor[attr])
                                    .attr('opacity', ()=>(attr=="lck")?0.4:(attr=="noise")?0.5:0.8)
                                    .attr("d", area(datum))
                            }

                            rect_size = 8
                            if (attr != "checkbox") {
                                svg.append("rect").attr("x", (xHigh - 4*rect_size) / 2).attr("y", -yHigh/2 + deltaLegend*rect_size).attr('width', rect_size).attr('height', rect_size).style("fill", pathColor[attr]).attr('class', 'legend')
                                svg.append("text").attr("x", (xHigh - 1*rect_size) / 2).attr("y", -yHigh/2 + (deltaLegend + 1)*rect_size).text(attr).style("font-size", "10px").style("fill", pathColor[attr]).attr('class', 'legend')
                                deltaLegend += 2
                            }
                        }
                    }

                // Title
                svg.append("text")
                    // .attr("x", -width/5)
                    .attr("class", "title")
                    .attr("y", -yHigh/2 + 10)
                    .attr("dy", "0em")
                    .style("fill", "rgb(18, 113, 249)")
                    .style("font-size", "15px")
                    .style("font-weight", "normal")
                    .style("text-anchor", "middle")
                    .text(`Radial View (${selectedId})`)

                    if (gridPlotted === true) {
                        // Creating a grid for reference
                        radius = Math.min(xHigh, yHigh) / 2 + 10;

                        // girdcircle for days of study
                        svg.selectAll(".gridCircles")
                        .data(d3.range(starting_min - 1, starting_max + 1, 1))
                        .enter()
                        .append("circle")
                        .attr("class", "gridCircles")
                        .attr("fill", "none")
                        // .style("fill", "url(#grad)")
                        .attr("stroke", "gray")
                        .attr("opacity", config.opacity)
                        .attr("stroke-width", 1 / 10)
                        .attr("r", function(d) {
                            return find_radius(d)
                        })

                        // grid lines for hours of the day
                        svg.selectAll(".gridLines")
                            .data(d3.range(0, 24, 1))
                            .enter()
                            .append("line")
                            .attr("class", 'gridLines')
                            .attr("x1", find_radius(starting_min - 1))
                            .attr("x2", find_radius(starting_max))
                            .attr("opacity", config.opacity)
                            .attr("stroke", "gray")
                            .attr("stroke-width", 1 / 10)
                            .attr("transform", function(d) { return `rotate(${hourScale(d)})` });

                        // labels for the hours of the day
                        svg.selectAll('.hourLabel')
                        .data(d3.range(0, 24, 1))
                        .enter()
                        .append('text')
                        .attr('class', 'hourLabel')
                        .attr('text-anchor', 'middle')
                        .style('font-size', '8px')
                        .style("cursor", "default")
                        .attr('x', function(d) {
                            return radius * Math.sin(hourScale(d) * radians);
                        })
                        .attr('y', function(d) {
                            if (d == 0) return -radius * Math.cos(hourScale(d) * radians) + 0;
                            else if (d == 12) return -radius * Math.cos(hourScale(d) * radians) + (hourLabelYOffset*2);
                            else return -radius * Math.cos(hourScale(d) * radians) + hourLabelYOffset;
                        })
                        .text(function(d) {
                            if (d == 0)
                                return "MidNight";
                            else if (d < 12)
                                return d + " am";
                            else if (d == 12)
                                return "MidDay";
                            else if (d > 12)
                                return d - 12 + " pm";
                        });

                        // lables for day number
                        var noDays = starting_max - starting_min
                        var inc = 1
                        if (noDays > 15 & noDays < 30)
                            inc = 2
                        else if (noDays > 30 & noDays < 50)
                            inc = 3
                        else if (noDays > 50)
                            inc = 5
                        daynumberdata = d3.range(starting_min, starting_max + 1, inc)

                        svg.selectAll('.dayLabel')
                            .data(daynumberdata)
                            .enter()
                            .append('text')
                            .attr("opacity", 0.8)
                            .attr('class', 'dayLabel')
                            .attr('text-anchor', 'middle')
                            .style('font-size', '8px')
                            .attr('x', 0)
                            .attr('y', function(d) { return find_radius(d) })
                            .text(function(d) {
                                return d;
                            })
                            .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px") })
                            .on('mouseover', function(d) {
                                tooltip.text(`${Object.keys(d2i).find(key => d2i[key] === d)}`);
                                d3.select(this).style("cursor", "default");
                                return tooltip.style("visibility", "visible");
                            })
                            .on('mouseout', function() {
                                tooltip.style("visibility", "hidden")
                            })

                        // .on('mouseover', function(d) {
                        //     d3.select(this)
                        //         // .attr('y', "-3em")
                        //         // .style('font-size', '2em')

                        //         .style("cursor", "default")
                        // })
                        // .on('mouseout', function(d) {
                        //     d3.select(this)
                        //         // .attr('y', "1em")
                        //         .style('font-size', '0.5em')
                        //         .style("fill", "black");
                        // });


                        // svg.append("circle").attr("cx",200).attr("cy",160).attr("r", 6).style("fill", "#404080")

                        // svg.append("text").attr("x", 220).attr("y", 160).text("variable B").style("font-size", "15px").attr("alignment-baseline","middle")
                    }
                }


                // Code for brush
                function brushSlider(min, max, starting_min = min, starting_max = max) {

                    var range = [min, max + 1]
                    var starting_range = [starting_min, starting_max]

                    // // set width and height of svg
                    // var margin = { top: 25, right: 25, bottom: 25, left: 25 },
                    //     width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
                    //     height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

                    // create x scale
                    var x = d3.scaleLinear()
                        .domain(range) // data space
                        .range([0, xHigh]); // display space

                    // create svg and translated g
                    var svg = d3.select('#' + chart)
                    var g = svg.append('g').attr("class", "brush").attr('transform', `translate(${margin.left}, ${yHigh})`)

                    // draw background lines
                    g.append('g').selectAll('line')
                        .data(d3.range(range[0], range[1] + 1))
                        .enter()
                        .append('line')
                        .attr('x1', d => x(d)).attr('x2', d => x(d))
                        .attr('y1', 0).attr('y2', margin.bottom / 1.5)
                        .style('stroke', '#ccc')

                    // labels
                    var labelL = g.append('text')
                        .attr('id', 'labelleft')
                        .attr('x', -10)
                        .attr('y', -5)
                        .style("font-size", "12px")
                        .style("font-weight", "normal")
                        .style("text-anchor", "middle")
                        .text(range[0])

                    var labelR = g.append('text')
                        .attr('id', 'labelright')
                        .attr('x', -10)
                        .attr('y', -5)
                        .style("font-size", "12px")
                        .style("font-weight", "normal")
                        .style("text-anchor", "middle")
                        .text(range[1])

                    // define brush
                    var brush = d3.brushX()
                        .extent([
                            [0, 0],
                            [xHigh, margin.bottom / 1.5]
                        ])
                        .on('brush', function() {
                            var s = d3.event.selection;
                            // update and move labels
                            labelL.attr('x', s[0] - 5)
                                .text(Math.round(x.invert(s[0])))
                            labelR.attr('x', s[1])
                                .text(Math.round(x.invert(s[1])) - 1)
                                // move brush handles      
                            handle.attr("display", null).attr("transform", function(d, i) { return "translate(" + [s[i], -margin.bottom / 2] + ")"; });
                            // update view
                            // if the view should only be updated after brushing is over, 
                            // move these two lines into the on('end') part below
                            svg.node().value = s.map(d => Math.round(x.invert(d)));
                            svg.node().dispatchEvent(new CustomEvent("input"));
                        })
                        .on('end', function() {
                            if (!d3.event.sourceEvent) return;

                            var d0 = d3.event.selection.map(x.invert);
                            var d1 = d0.map(Math.round)
                            var starting_min = d1[0]
                            var starting_max = d1[1] - 1
                            if (starting_min <= starting_max) {
                                d3.select(this).transition().call(d3.event.target.move, d1.map(x))

                                d3.select("#" + chart).selectAll('.areaPath').remove();
                                d3.select("#" + chart).selectAll('.title').remove();
                                d3.select("#" + chart).selectAll('.gridCircles').remove();
                                d3.select("#" + chart).selectAll('.gridLines').remove();
                                d3.select("#" + chart).selectAll('.hourLabel').remove();
                                d3.select("#" + chart).selectAll('.dayLabel').remove();
                                deltaLegend = 1;

                                plotRadial(starting_min, starting_max)
                                starting_min_date = Object.keys(d2i).find(key => d2i[key] === starting_min)
                                starting_max_date = Object.keys(d2i).find(key => d2i[key] === starting_max)

                                if ($("#featureType").is(':checked')) {
                                    featureType = "individualFeatures"
                                } else {
                                    featureType = "aggregatedFeatures"
                                }

                                if (featureType == "individualFeatures"){
                                    updateParallelCord(dependentChart1, selectedId, lassoSelectedIds=[], featureType, featurelist, classLabel, labels, starting_min_date, starting_max_date)
                                }
                            }

                        })

                    // append brush to g
                    var gBrush = g.append("g")
                        .attr("class", "brush")
                        .call(brush)

                    // add brush handles (from https://bl.ocks.org/Fil/2d43867ba1f36a05459c7113c7f6f98a)
                    var brushResizePath = function(d) {
                        var e = +(d.type == "e"),
                            x = e ? 1 : -1,
                            y = margin.bottom / 1.75;
                        return "M" + (.5 * x) + "," + y + "A6,6 0 0 " + e + " " + (6.5 * x) + "," + (y + 6) + "V" + (2 * y - 6) +
                            "A6,6 0 0 " + e + " " + (.5 * x) + "," + (2 * y) + "Z" + "M" + (2.5 * x) + "," + (y + 8) + "V" + (2 * y - 8) +
                            "M" + (4.5 * x) + "," + (y + 8) + "V" + (2 * y - 8);
                    }

                    var handle = gBrush.selectAll(".handle--custom")
                        .data([{ type: "w" }, { type: "e" }])
                        .enter().append("path")
                        .attr("class", "handle--custom")
                        .attr("stroke", "#000")
                        .attr("fill", '#eee')
                        .attr("cursor", "ew-resize")
                        .attr("d", brushResizePath);

                    // override default behaviour - clicking outside of the selected area 
                    // will select a small piece there rather than deselecting everything
                    // https://bl.ocks.org/mbostock/6498000
                    gBrush.selectAll(".overlay")
                        .each(function(d) { d.type = "selection"; })
                        .on("mousedown touchstart", brushcentered)

                    function brushcentered() {
                        var dx = x(7) - x(0), // Use a fixed width when recentering.
                            cx = d3.mouse(this)[0],
                            x0 = cx - dx / 2,
                            x1 = cx + dx / 2;
                        d3.select(this.parentNode).call(brush.move, x1 > xHigh ? [xHigh - dx, xHigh] : x0 < 0 ? [0, dx] : [x0, x1]);
                    }

                    // select entire starting range
                    gBrush.call(brush.move, starting_range.map(x))

                    // return svg.node()
                    return [range[0], range[1]]
                }

                //for plotting the sensor measurements in the form of circular area chart
                d3.select("#" + chart).selectAll('*').remove();
                if (!(Object.keys(attributesTemp).every((k) => attributesTemp[k] == false & k != "checkbox"))) {
                    brushSlider(min = sliderMin, max = sliderMax, starting_min, starting_max + 1);
                }
                plotRadial(starting_min, starting_max)
                
                // remove the buffering logo
                d3.select("#" + chart).selectAll('.buffer').remove();
            })

    return true, true;
}


function updateRadialTime(chart, dependentChart1, selectedId, featureType, featurelist, classLabel, labels, brtChecked, accChecked, gyrChecked, lckChecked, sleepNoiseChecked) {
    /* This method is used to call the plotting method for different sensor attributes*/

    buffering(chart, selectedId); //calling method that plots buffering symbol

    attributes = { "acc": accChecked, "gyro": gyrChecked, "brt": brtChecked, "lck": lckChecked, "noise": sleepNoiseChecked }
    // attributes = { "acc": accChecked, "gyro": gyrChecked, "brt": brtChecked, "lck": lckChecked}
    radialTime(chart, dependentChart1, selectedId, featureType, featurelist, classLabel, labels, attributes)
}