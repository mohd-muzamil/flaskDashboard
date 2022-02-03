function plotAreaChart(chart, participantId, attributes) {
    var chart = chart
    var participantId = participantId
    var attributes = attributes
    var pathColor = {"brt": "#1b9e77", "acc": "#d95f02", "gyr": "#7570b3"}
    var gridPlotted = false

    var postForm = { //Fetch form data
        // 'filename': filename, //Store name fields value
        'participantId': participantId, //Store name fields value
        "attributes" : attributes
    };

    //fetcing filtered participant data from flask server
    d3.csv("/filterParticipants")
        .header("Content-Type", "application/json")
        .post(JSON.stringify(postForm),
            function(data) {
                d3.select("#" + chart).selectAll('g').remove();     //clearing the chart before plotting new data
                data.forEach(function(d) {
                    // d.date = parseDate(d.date);
                    d.minuteOfTheDay = +d.minuteOfTheDay;
                    d.brt = +d.brt;
                    d.acc = +d.acc;
                    d.gyr = +d.gyr;
                });

                dates = Array.from(new Set(data.map(d => d.date)).values()).sort();
                d2i = {};
                dates.forEach((d, i) => d2i[d] = i+1);
                numDates = Object.keys(dates).length

                var sliderMin = 1
                var sliderMax = numDates
                var starting_min = 1
                var starting_max = numDates

                plotRadial(starting_min, starting_max)
                    brushSlider(min = sliderMin, max = sliderMax, starting_min, starting_max+1);
                // sliderMin = sliderValues[0]
                // sliderMax = sliderValues[1]
                
                // plotRadier function here
                function plotRadial(starting_min, starting_max){
                    const config = {
                        opacity: 0.8,
                        strokewidth: 1
                    }
                
                    var radians = 0.0174532925,
                        hourLabelYOffset = 7;
                
                    // Set the dimensions of the canvas / graph
                    var margin = { top: 25, right: 25, bottom: 75, left: 25 },
                        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
                        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
                    // Parse the date / time
                    var parseDate = d3.timeFormat("%Y-%m-%d");
                
                    // var arcGenerator = d3.arc();
                
                    // Select the svg
                    var svg = d3.select("#" + chart)
                        .attr("width", width)
                        .attr("height", height)
                        .append('g')
                        .attr("transform", `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top/2 + height + margin.bottom) / 2})`);
                
                    var find_radius = d3.scaleLinear()
                        // .domain(d3.extent(data, function(d) { return + (new Date(...d.date.split("-").map((x)=>(+x)))); }))
                        .domain([starting_min-1, starting_max])
                        .range([Math.min(height, width) / 8, Math.min(height, width) / 2]);
                
                    var hourScale = d3.scaleLinear()
                        .domain([0, 24])
                        .range([0, 360]);
                
                    x = d3.scaleLinear()
                        .domain([0, 1440])
                        .range([0, 2 * Math.PI]);
                    
                    for (let i=0; i<Object.keys(attributes).length; i++){
                        attr = Object.keys(attributes)[i]
                        if (attributes[attr]){
                            // d3.range(starting_min, starting_max)((d, i) =>
                            for (let d=starting_min; d<=starting_max; d++){
                                currDate = d;
                        
                                datum = data.filter(function(row, i) {
                                    return d2i[row['date']] == currDate && row[attr] != NaN;
                                })
                        
                                y = d3.scaleLinear()
                                    .domain(d3.extent(datum, function(d) { return d[attr]; }))
                                    .range([find_radius(currDate-1), find_radius(currDate)]);
                        
                                const area = d3.areaRadial()
                                    .angle(d => x(d.minuteOfTheDay))
                                    .innerRadius(d => y(0))
                                    .outerRadius(d => y(d[attr]));
                                
                                var xScale = d3.scaleLinear()
                                    .domain([0, 6])
                                    .range([0, 2 * Math.PI]);

                                var yScale = d3.scaleLinear()
                                    .domain([0, 20])
                                    .range([width/2, height/2]);
                        
                                // Add the line
                                svg.append("path")
                                .attr("class", "areaPath")
                                .attr("fill", pathColor[attr])
                                .attr('opacity', 1)
                                .attr("stroke", "black")
                                .attr("stroke-width", 1 / 20)
                                .attr("d", area(datum))
                        
                                d3.select("#" + chart).selectAll('.buffer').remove();
                            }
                        }
                    }
                
                    if (gridPlotted === false) {
                        // Creating a grid for reference
                        radius = Math.min(width, height) / 2 + 15;
                
                        // var grad = svg.append("defs")
                        //     .append("linearGradient").attr("id", "grad")
                        //     .attr("x1", "0%").attr("x2", "0%").attr("y1", "100%").attr("y2", "0%");
                
                        // grad.append("stop").attr("offset", "50%").style("stop-color", "lightblue");
                        // grad.append("stop").attr("offset", "50%").style("stop-color", "white");
                
                        svg.append("text")
                        // .attr("x", -width/5)
                        .attr("y", -margin.top - height/2)
                        .attr("dy", "-0.1em")
                        .style("font-size", "12px")
                        .style("font-weight", "normal")
                        .style("text-anchor", "middle")
                        .text("Participant: "+participantId)
                
                        svg.selectAll(".gridCircles")
                            .data(d3.range(starting_min-1, starting_max+1, 1))
                            .enter()
                            .append("circle")
                            .attr("class", "gridCircles")
                            .attr("fill", "none")
                            // .style("fill", "url(#grad)")
                            .attr("stroke", "black")
                            .attr("opacity", config.opacity)
                            .attr("stroke-width", 1 / 10)
                            .attr("r", function(d) {
                                return find_radius(d)
                            })
                
                        svg.selectAll(".gridLines")
                            .data(d3.range(0, 24, 1))
                            .enter()
                            .append("line")
                            .attr("class", 'gridLines')
                            .attr("x1", find_radius(starting_min-1))
                            .attr("x2", find_radius(starting_max))
                            .attr("opacity", config.opacity)
                            .attr("stroke", "black")
                            .attr("stroke-width", 1 / 10)
                            .attr("transform", function(d) { return `rotate(${hourScale(d)})` });
                
                        svg.selectAll('.hourLabel')
                            .data(d3.range(0, 24, 1))
                            .enter()
                            .append('text')
                            .attr('class', 'hourLabel')
                            .attr('text-anchor', 'middle')
                            .style('font-size', '10px')
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
                            .data(d3.range(starting_min, starting_max+1, 1))
                            .enter()
                            .append('text')
                            .attr('class', 'dayLabel')
                            .attr('text-anchor', 'middle')
                            .style('font-size', '0.5em')
                            .attr('x', 0)
                            .attr('y', function(d) {return find_radius(d)})
                            .text(function(d) {
                                return d;
                            })
                            .on('mouseover', function(d) {
                                d3.select(this)
                                    // .attr('y', "-3em")
                                    .style('font-size', '2em')
                                    .style("cursor", "default")
                            })
                            .on('mouseout', function(d) {
                                d3.select(this)
                                    // .attr('y', "1em")
                                    .style('font-size', '0.5em')
                                    .style("fill", "black");
                            });
                    }       
                        //remove the loading symbol
                        d3.select("#" + chart).selectAll('.buffer').remove();
                        
                }

                // Code for brush
            function brushSlider(min, max, starting_min = min, starting_max = max) {

                var range = [min, max+1]
                var starting_range = [starting_min, starting_max]
            
                // set width and height of svg
                var margin = { top: 25, right: 25, bottom: 25, left: 25 },
                    width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
                    height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
            
                // create x scale
                var x = d3.scaleLinear()
                    .domain(range) // data space
                    .range([0, width]); // display space
            
                // create svg and translated g
                var svg = d3.select('#' + chart)
                var g = svg.append('g').attr("class", "brush").attr('transform', `translate(${margin.left}, ${height + 1.25*(margin.bottom)})`)
            
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
                        [width, margin.bottom / 1.5]
                    ])
                    .on('brush', function() {
                        var s = d3.event.selection;
                        // update and move labels
                        labelL.attr('x', s[0]-5)
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
                        if (d1[0]<d1[1]){
                            d3.select(this).transition().call(d3.event.target.move, d1.map(x))
                            
                            d3.select("#" + chart).selectAll('.areaPath').remove();
                            d3.select("#" + chart).selectAll('.gridCircles').remove();
                            d3.select("#" + chart).selectAll('.gridLines').remove();
                            d3.select("#" + chart).selectAll('.hourLabel').remove();
                            d3.select("#" + chart).selectAll('.dayLabel').remove();
                            
                            plotRadial(d1[0], d1[1]-1)
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
                    d3.select(this.parentNode).call(brush.move, x1 > width ? [width - dx, width] : x0 < 0 ? [0, dx] : [x0, x1]);
                }
            
                // select entire starting range
                gBrush.call(brush.move, starting_range.map(x))
            
                // return svg.node()
                return [range[0], range[1]]
            }

            })

            

    return true, true;
}




// function createGrid(chart) {
//     // Set the dimensions of the canvas / graph
//     var margin = { top: 25, right: 25, bottom: 25, left: 25 },
//         width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
//         height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

//     // Select the svg
//     var svg = d3.select("#" + chart)
//         .attr("width", width)
//         .attr("height", height)
//         .append('g')
//         .attr("transform", `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom) / 2})`);
// }

function updatePlotAreaChart(chart, participantId, brtChecked, accChecked, gyrChecked, lckChecked) {
    /* This method is used to call the plotting method for different sensor attributes*/

    d3.select("#" + chart).selectAll('g').remove();     //clearing the chart before plotting new data
    buffering(chart, participantId);       //calling method that plots buffering symbol

    // gridPlotted = false;
    // brushPlotted = false;
    attributes = {"brt":brtChecked, "acc":accChecked, "gyr":gyrChecked}

    // brightnessData
    // filename = "dummyBrightness";
    // attr = "brt";
    // pathColor = "green";
    
    plotAreaChart(chart, participantId, attributes)

    // //accelerometerData
    // if (accChecked == true) {
    //     filename = "dummyAccelerometer";
    //     attr = "acc";
    //     pathColor = "red";
    //     brushPlotted, gridPlotted = plotAreaChart(chart, participantId, filename, attr, pathColor, gridPlotted, brushPlotted)
    // }
    // //gyroscopeData
    // if (gyrChecked == true) {
    //     filename = "dummyGyroscope";
    //     attr = "gyr";
    //     pathColor = "blue";
    //     brushPlotted, gridPlotted = plotAreaChart(chart, participantId, filename, attr, pathColor, gridPlotted, brushPlotted)
    // }
    // //lockstateData
    // if (lckChecked == true) {
    //     pathColor = "purple";
    //     datapath = "../../data/lockstate_d3";
    //     attr = "lck";
    // }
}