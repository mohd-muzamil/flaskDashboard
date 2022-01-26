//This script is used to plot radial glyphs in first svg
const radialGlyph = (chart, dependendChart, radius, brtChecked, accChecked, gyrChecked, lckChecked) => {
    const config = {
        r: +radius,
        opacityLow: 0,
        opacityHigh: 0.7,
        strokeWidthLow: 0,
        strokeWidthHigh: 0.5,
        fillColorHover: "#ddd",
        fillColor: "rgb(255, 255, 255)"
    }

    const margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

    const svg1 = d3.select("#" + chart)
        .append('g')
        //     .attr("width", width)
        //     .attr("height", height)

    // tooltip
    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style('font-size', '1em')
        .style("border-width", "2px")
        .style("padding", "5px")
        .style('background-color', 'white')
        .style('border-radius', '10% 10% 10% 10%');

    // reading data
    //d3.csv("../../data/participant_scores", function(error, data) {
    d3.csv("../../data/dummyPersonalityScores", function(error, data) {
        data.forEach(d => {
            d.x = +d.x
            d.y = +d.y
        });

        const xScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.x)))
            .range([margin.left + config.r, width - margin.right - config.r])


        const yScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.y)))
            .range([height - margin.bottom - config.r, margin.top + config.r])


        const radialLine = d3.lineRadial()
        const radialScale = d3.scaleLinear()
            .domain([0, 10])
            .range([0, config.r])



        // Add a clipPath: everything out of this area won't be drawn.
        // var clip = svg1.append("defs").append("svg:clipPath")
        //     .attr("id", "clip")
        //     .append("svg:rect")
        //     .attr("width", width)
        //     .attr("height", height)
        //     .attr("x", 0)
        //     .attr("y", 0);

        // Add brushing
        var brush = d3.brush() // Add the brush feature using the d3.brush function
            .extent([
                [0, 0],
                [`${margin.left + width + margin.right}`, `${margin.top + height + margin.bottom}`]
            ]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
            .on("end", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

        // Create the scatter variable: where both the circles and the brush take place
        var scatter = svg1.append('g')
            .attr("clip-path", "url(#clip)")

        // RadialGlyph
        scatter.selectAll('circle')
            .data(data)
            .enter()
            .each(function(d) {
                d3.select(this)
                    .append('g')
                    .selectAll('path')
                    .data([d])
                    .enter()
                    .append('path')
                    .attr('d', d => radialLine([
                        d.open,
                        d.con,
                        d.extra,
                        d.agree,
                        10 - d.neuro,
                        d.open
                    ].map((v, i) => [Math.PI * (i) / 2.5, radialScale(v)])))
                    .attr('transform', `translate(${xScale(d.x)}, ${yScale(d.y)})`)
                    // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'black')
                    .attr('stroke', 'black')
                    .attr('stroke-width', config.strokeWidthHigh)
                    // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'blue')
                    .attr('fill', d => d.device == "ios" ? "red" : "black") //use this coloring for showing device type ios or android, can also show cluster
                    .attr('opacity', config.opacityHigh)
            });



        // Add the brushing
        scatter
            .append("g")
            .attr("class", "brush")
            .call(brush);

        // A function that set idleTimeOut to null
        var idleTimeout

        function idled() { idleTimeout = null; }

        // A function that update the chart for given boundaries
        function updateChart() {
            extent = d3.event.selection
                // If no selection, back to initial coordinate. Otherwise, update X axis domain
            if (!extent) {
                if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
                xScale.domain(d3.extent(data.map(d => d.x)))
                yScale.domain(d3.extent(data.map(d => d.y)))

            } else {
                // svg1.selectAll('.glyph').remove();
                xScale.domain([xScale.invert(extent[0][0]), xScale.invert(extent[1][0])])
                yScale.domain([yScale.invert(extent[1][1]), yScale.invert(extent[0][1])])
                tooltip.style("visibility", "hidden")
                svg1.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
            }

            // // Update axis and circle position
            // xAxis.transition().duration(1000).call(d3.axisBottom(x))
            scatter.selectAll("path").remove()
            scatter.selectAll("circle").remove()

            scatter.selectAll('circle')
                .data(data)
                .enter()
                .each(function(d) {
                    d3.select(this)
                        .append('g')
                        .selectAll('path')
                        .data([d])
                        .enter()
                        .append('path')
                        .attr('d', d => radialLine([
                            d.open,
                            d.con,
                            d.extra,
                            d.agree,
                            10 - d.neuro,
                            d.open
                        ].map((v, i) => [Math.PI * (i) / 2.5, radialScale(v)])))
                        .attr('transform', `translate(${xScale(d.x)}, ${yScale(d.y)})`)
                        // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'black')
                        .attr('stroke', 'black')
                        .attr('stroke-width', config.strokeWidthHigh)
                        // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'blue')
                        .attr('fill', d => d.device == "ios" ? "red" : "black") //use this coloring for showing device type ios or android, can also show cluster
                        .attr('opacity', config.opacityHigh)
                });

            // let current_circle = undefined;

            scatter.selectAll('circle')
                .data(data)
                .enter()
                .append('circle')
                .attr("cx", function(d) { return xScale(d.x); })
                .attr("cy", function(d) { return yScale(d.y); })
                .attr("r", config.r)
                .style("fill", config.fillColor)
                .attr('opacity', config.opacityLow)
                .attr('stroke', 'black')
                .attr('stroke-width', config.strokeWidthLow)
                .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px") })
                .on('mouseover', function(d) {
                    d3.select(this)
                        .attr("opacity", config.opacityHigh)
                        .style('fill', config.fillColorHover)
                        .attr('stroke-width', config.strokeWidthHigh)
                    tooltip.text(`${d.participantId} O:${Math.floor(d.open)} C:${Math.floor(d.con)} E:${Math.floor(d.extra)} A:${Math.floor(d.agree)} N:${Math.floor(d.neuro)}`);
                    return tooltip.style("visibility", "visible");
                })
                .on('mouseout', function() {
                    if (d3.select(this).attr("class") != "selectedGlyph")
                        d3.select(this)
                        .attr("opacity", config.opacityLow)
                        .attr('stroke-width', config.strokeWidthLow)
                        .style("fill", config.fillColor);
                    tooltip.style("visibility", "hidden")
                })
                .on("click", function(d) {
                    // click on unselected point
                    if (d3.select(this).attr("class") != "selectedGlyph") {
                        svg1.selectAll('.selectedGlyph')
                            .classed('selectedGlyph', false)
                            .attr("opacity", config.opacityLow)
                            .attr("stroke-width", config.strokeWidthLow)
                            .style("fill", config.fillColor);

                        d3.select(this).classed('selectedGlyph', true)
                            .attr("opacity", config.opacityHigh)
                            .attr("stroke-width", config.strokeWidthHigh * 2);

                        // click on selected point
                    } else {
                        d3.select(this).classed('selectedGlyph', false);
                        d3.select(this)
                            .attr("opacity", config.opacityLow)
                            .attr('strokeWidth', config.strokeWidthLow)
                            .style("fill", config.fillColor);
                    }
                    updateglyph_test(dependendChart, d.participantId, brtChecked, accChecked, gyrChecked, lckChecked)
                    
                });

            scatter.selectAll('text')
                .data(data)
                .enter()
                .append("text")
                .attr("x", function(d) { return xScale(d.x); })
                .attr("y", function(d) { return yScale(d.y); })
                .attr("dx", "-15px")
                .attr("dy", "-10px")
                .attr("font-size", "0.7em")
                .text(function(d) {
                    // return d.participantId.includes() ? d.participantId : "";
                    if (["PROSITC0003", "PROSITC0007", "PROSITC0008", "Test"].some(v => d.participantId.includes(v))) {
                        return d.participantId
                    } else { return "" }
                })

        }

        // let current_circle = undefined;

        scatter.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr("cx", function(d) { return xScale(d.x); })
            .attr("cy", function(d) { return yScale(d.y); })
            .attr("r", config.r)
            .style("fill", config.fillColor)
            .attr('opacity', config.opacityLow)
            .attr('stroke', 'black')
            .attr('stroke-width', config.strokeWidthLow)
            .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px") })
            .on('mouseover', function(d) {
                d3.select(this)
                    .attr("opacity", config.opacityHigh)
                    .style('fill', config.fillColorHover)
                    .attr('stroke-width', config.strokeWidthHigh)
                tooltip.text(`${d.participantId} O:${Math.floor(d.open)} C:${Math.floor(d.con)} E:${Math.floor(d.extra)} A:${Math.floor(d.agree)} N:${Math.floor(d.neuro)}`);
                return tooltip.style("visibility", "visible");
            })
            .on('mouseout', function() {
                if (d3.select(this).attr("class") != "selectedGlyph")
                    d3.select(this)
                    .attr("opacity", config.opacityLow)
                    .attr('stroke-width', config.strokeWidthLow)
                    .style("fill", config.fillColor);
                tooltip.style("visibility", "hidden")
            })
            .on("click", function(d) {
                // click on unselected point
                if (d3.select(this).attr("class") != "selectedGlyph") {
                    svg1.selectAll('.selectedGlyph')
                        .classed('selectedGlyph', false)
                        .attr("opacity", config.opacityLow)
                        .attr("stroke-width", config.strokeWidthLow)
                        .style("fill", config.fillColor);

                    d3.select(this).classed('selectedGlyph', true)
                        .attr("opacity", config.opacityHigh)
                        .attr("stroke-width", config.strokeWidthHigh * 2);

                    // click on selected point
                } else {
                    d3.select(this).classed('selectedGlyph', false);
                    d3.select(this)
                        .attr("opacity", config.opacityLow)
                        .attr('strokeWidth', config.strokeWidthLow)
                        .style("fill", config.fillColor);
                }
                updateglyph_test(dependendChart, d.participantId, brtChecked, accChecked, gyrChecked, lckChecked)
            });

        scatter.selectAll('text')
            .data(data)
            .enter()
            .append("text")
            .attr("x", function(d) { return xScale(d.x); })
            .attr("y", function(d) { return yScale(d.y); })
            .attr("dx", "-15px")
            .attr("dy", "-10px")
            .attr("font-size", "0.7em")
            .text(function(d) {
                // return d.participantId.includes() ? d.participantId : "";
                if (["PROSITC0003", "PROSITC0007", "PROSITC0008", "Test"].some(v => d.participantId.includes(v))) {
                    return d.participantId
                } else { return "" }
            })





    })
}

function updateRadialGlyphs(chart, dependendChart, radius, brtChecked, accChecked, gyrChecked, lckChecked) {
    d3.select("#" + chart).selectAll('g').remove();
    d3.select("#" + dependendChart).selectAll('g').remove();
    radialGlyph(chart, dependendChart, radius, brtChecked, accChecked, gyrChecked, lckChecked)
}