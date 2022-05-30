// This script is used to generate visual representations over Feature comparison View.
// d3V4 implementation of code similar to that by Mike Bostock
// https://bl.ocks.org/mbostock/1341021
// https://gist.github.com/kotomiDu/d1fd0fe9397db41f5f8ce1bfb92ad20d
// https://gist.github.com/titipignataro/47135818bad65a439174038227e0eb20

function parallelCord(chart, selectedId, lassoSelectedIds, featuresType, featurelist, classLabel , labels, starting_min_date, starting_max_date) {
    console.log(selectedId, lassoSelectedIds)
    var featuresNames
    var importanceScores
    const line_color = "#525252"
    const titleLegend = "Feature Importance"

    postForm = { "featureColumns": featurelist, "classLabel": classLabel }
    $.ajax({
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(postForm),
        url: "/getFeatureImportance",
        async: false,
        success: function(data) {
            featuresNames = Object.keys(data)
            importanceScores = Object.values(data)
        }
    })

    var margin = { left: 20, top: 20, right: 40, bottom: 20 },
        width = Math.floor(+$("#" + chart).width()),
        height = Math.floor(+$("#" + chart).height()),
        xHigh = (width - margin.left - margin.right),
        yHigh = (height - margin.top - margin.bottom)

    if (featuresType == "aggregatedFeatures") {
        serverRoute = "/getAggFeatures"
        titleText = "Aggregated features of all the selectedIds over Study period"
        featureLength = featurelist.length
        if (featuresNames.includes("date_num")) {
            const index = featuresNames.indexOf("date_num");
            if (index > -1) {
                featuresNames.splice(index, 1); // 2nd parameter means remove one item only
            }
        }
    } else if (featuresType == "individualFeatures") {
        serverRoute = "/getIndividualFeatures"
        titleText = "Day-wise features - selectedId:" + selectedId
        featureLength = featurelist.length - 1
        if (!featuresNames.includes("date_num")) {
            featuresNames.unshift("date_num")
            importanceScores.unshift(0)
        }
    }

    var deltaWidth = 0
    if (featurelist.length > 1) {
        deltaWidth = (20 - featurelist.length) * xHigh / 40
        xHigh = xHigh - deltaWidth
    }

    var featuresCodes = featuresNames
    const colorClusters = d3.scaleOrdinal().domain(labels).range(d3.schemeCategory10)

    const featureImportanceScale = d3.scaleSequential(d3.interpolate("#3f007d", "#FFFFFF")).domain([1, 0])

    console.log(featuresNames, featuresCodes)
    var x = d3.scalePoint().domain(featuresCodes).range([margin.left, xHigh - margin.right]),
        y = {},
        formatDecimal = d3.format(".0f");

    var line = d3.line(),
        background,
        foreground;

    const svg = d3.select("#" + chart)
        .attr("width", margin.left + width + margin.right)
        .attr("height", margin.top + height + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left + deltaWidth/2}, ${margin.top})`)

    var tooltip = d3.select("body")
        .append("div")
        .attr("class", "Tooltip")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("font-size", "12px")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "1px")
        .style("border-radius", "5px")
        .style("padding", "1px")
        .style("pointer-events", "none")
        .style("opacity", 0.8)

    postForm = { "id": selectedId }
    dragging = {}


    d3.csv(serverRoute)
        .header("Content-Type", "application/json")
        .post(JSON.stringify(postForm),
            function(data) {
                var filteredData = data
                if (featuresType == "aggregatedFeatures") {
                    if (lassoSelectedIds.length > 1) {
                        filteredData = data.filter(d => {
                            if (lassoSelectedIds.includes(d.id))
                                return d
                        })
                    }
                } else if (featuresType == "individualFeatures" & (starting_min_date != "" | starting_max_date != "")) {
                    var filteredData = data.filter((d) => {
                        if (d.date >= starting_min_date & d.date <= starting_max_date)
                            return d
                    })
                }

                // var date_num = [...new Set(filteredData.map(d => d["date_num"]))]

                // Create a scale and brush for each trait.
                featuresCodes.forEach(function(d) {
                    // Coerce values to numbers.
                    if (d == "date_num") {
                        data.forEach(function(p) { p[d] = formatDecimal(p[d]) });
                        y[d] = d3.scaleLinear()
                            .domain(d3.extent(data, function(p) { return +p[d]; }))
                            .range([yHigh, 0])
                    } else {
                        data.forEach(function(p) { p[d] = +p[d] });
                        min = d3.extent(data, function(p) { return +p[d]; })[0]
                        max = d3.extent(data, function(p) { return +p[d]; })[1]
                        y[d] = d3.scaleLinear()
                            .domain([0, max])
                            .range([yHigh, 0]);
                    }
                });

                // Add gray background lines for context.
                background = svg.append("svg:g")
                    .attr("class", "background")
                    .selectAll("path")
                    .raise()
                    .data(data)
                    .enter().append("svg:path")
                    .attr("d", path)

                // Add a title to svg.
                svg.append("text")
                    .attr("x", xHigh / 2)
                    .attr("y", -margin.top + 15)
                    .style("fill", "rgb(18, 113, 249)")
                    .style("font-size", "15px")
                    .style("font-weight", "normal")
                    .style("text-anchor", "middle")
                    .text(titleText)

                // sequential Color legend for feature importance.
                var colorLegend = d3.legendColor()
                    .labelFormat(d3.format(".1f"))
                    .scale(featureImportanceScale)
                    .cells(11)
                    .shapePadding(-5)
                    .shapeWidth(16)
                    .shapeHeight(yHigh / 5)

                svg.append("g")
                    .attr("class", "legend")
                    .attr("transform", `translate(${xHigh + deltaWidth/2}, ${0}) scale(${0.5})`)
                    .call(colorLegend)
                    .style("opacity", 1);

                //Add a title to legend
                svg.append("text")
                    .attr("transform", `translate(${xHigh + deltaWidth/2},${xHigh/50}) scale(${yHigh/235})`)
                    .attr("font-size", "12px")
                    .attr("text-anchor", "middle")
                    .style("font-weight", "normal")
                    .selectAll("tspan")
                    .data(titleLegend.split(""))
                    .enter().append("tspan")
                    .attr("x", "-1em")
                    .attr("dy", "0.8em")
                    .text(function(d) { return d; });

                // Add foreground lines.
                foreground = svg.append("svg:g")
                    .attr("class", "foreground")
                    .selectAll("path")
                    .raise()
                    .data(filteredData)
                    .enter().append("svg:path")
                    .attr("d", path)
                    .attr("opacity", function(d) {
                        if (featuresType == "aggregatedFeatures") {
                            return d.id == selectedId ? 1 : 0.8
                        } else {
                            return 1
                        }
                    })
                    .attr("stroke", function(d) {
                        if (featuresType == "aggregatedFeatures") {
                            if(d.id == selectedId){console.log(d)}
                            return d.id != selectedId ?  colorClusters(d[classLabel]) : "#000";
                        } else {
                            return line_color
                        }
                    })
                    .attr("stroke-width", function(d) {
                        if (featuresType == "aggregatedFeatures") {
                            return d.id != selectedId ? "1px" : "2px";
                        } else {
                            return "1px"
                        }
                    })


                // Add a group element for each trait.
                var g = svg.selectAll(".featuresCodes")
                    .data(featuresCodes)
                    .enter().append("svg:g")
                    .attr("class", "featuresCodes")
                    .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
                    .call(d3.drag()
                        .subject(function(d) { return { x: x(d) }; })
                        .on("start", function(d) {
                            dragging[d] = x(d);
                            // background.attr("visibility", "hidden");
                        })
                        .on("drag", function(d) {
                            dragging[d] = Math.min(width, Math.max(0, d3.event.x));
                            foreground.attr("d", path)
                            background.attr("d", path)
                            featuresCodes.sort(function(a, b) { return position(a) - position(b); });
                            x.domain(featuresCodes);
                            g.attr("transform", function(d) { return "translate(" + position(d) + ")"; })
                        })
                        .on("end", function(d) {
                            delete dragging[d];
                            transition(d3.select(this)).attr("transform", "translate(" + x(d) + ")");
                            transition(foreground).attr("d", path);
                            transition(background).attr("d", path);
                        })
                    );
                
                // add boxes behind each axis 
                g.append("svg:g")
                    .attr("class", "featureImportance")
                    .filter(d=>{ if(d!="date_num"){return d} })
                    .each(function(d) { d3.select(this).append("rect") })
                    .append("rect")
                    .attr("class", "boxes")
                    .attr("width", 4)
                    .attr("height", yHigh)
                    .attr("fill", function(d, i) {
                        return featureImportanceScale(importanceScores[i])
                    })
                    .attr("stroke", "black")
                    .attr("stroke-width", 0.4)
                    .attr("opacity", 1)

            
                // Add an axis and title.
                g.append("g")
                    .attr("class", "axis")
                    .each(function(d) { d3.select(this).call(d3.axisLeft(y[d])); })
                    .append("svg:text")
                    .style("fill", "rgb(18, 113, 249)")
                    .style("font-size", "12px")
                    .style("font-weight", "normal")
                    .style("text-anchor", "middle")
                    .attr("text-anchor", "middle")
                    .attr("y", -0)
                    .attr("transform", `translate(${0}, ${yHigh + margin.bottom * 0.75}) rotate(-45)`)
                    .text(d => { return d })
                    .on("mousemove", function(d) {
                        // if (d3.event.pageX > 0.95 * width) {
                        //     if (d.length < 15) return tooltip.style("top", (d3.event.pageY + 1) + "px").style("left", (d3.event.pageX - 2 * deltawidth) + "px")
                        //     else return tooltip.style("top", (d3.event.pageY + 1) + "px").style("left", (d3.event.pageX - 3.5 * deltawidth) + "px")
                        // } else { return tooltip.style("top", (d3.event.pageY + 1) + "px").style("left", (d3.event.pageX - deltawidth) + "px") }
                        X = d3.event.pageX + 15
                        Y = d3.event.pageY + 10
                        return tooltip.style("left", X + "px").style("top", Y + "px")
                    })
                    .on('mouseover', function(d) {
                        tooltip.text(d);
                        return tooltip.style("visibility", "visible");
                    })
                    .on('mouseout', function() {
                        return tooltip.style("visibility", "hidden");
                    })

                function position(d) {
                    var v = dragging[d];
                    return v == null ? x(d) : v;
                }

                function transition(g) {
                    return g.transition().duration(750);
                }

                // Returns the path for a given data point.
                function path(d) {
                    return line(featuresCodes.map(function(p) {
                        return [position(p), y[p](d[p])];
                    }));
                }

                if (featuresType == "aggregatedFeatures") {
                    foreground.classed("fade", function(d, i) {
                        if (lassoSelectedIds.includes(d.id)) {
                            return d
                        }
                    });
                }
                d3.select("#" + chart).selectAll('.buffer').remove();
            });
}


function updateParallelCord(chart, selectedId, lassoSelectedIds, featuresType, featurelist, classLabel, labels, starting_min_date = "", starting_max_date = "") {
    // featuresType: aggregatedFeatures/individualFeatures
    if (Array.isArray(selectedId)) {
        selectedId = selectedId[0]
    }
    d3.select("#" + chart).selectAll('*').exit().remove(); //clearing the chart before plotting new data
    
    if (featuresType == "aggregatedFeatures") {
        buffering(chart, selectedId, toggleText = false)
    }
    else if (featuresType == "individualFeatures") {
        buffering(chart, selectedId)
    }
    parallelCord(chart, selectedId, lassoSelectedIds, featuresType, featurelist, classLabel, labels, starting_min_date, starting_max_date)
}