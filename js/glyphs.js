/****Importatnt file****/
// This script is used to plot glyphs in first svg

function glyphs(chart, dependendChart1, dependendChart2, dependendChart3, selectedParticipants, featurelist, radius, glyph, labels, brtChecked, accChecked, gyrChecked, lckChecked) {
    const config = {
        r: +radius,
        opacityLow: 0,
        opacityHigh: 0.85,
        strokeWidthLow: 0,
        strokeWidthHigh: 0.5,
        fillColorHover: "#ddd",
        fillColor: "rgb(255, 255, 255)",
        petals: 5, //no of petals in the glyph
        labelSize: radius/2, //size of labels to show over the glyphs
    }

    
    var selectedParticipantId = "";

    const margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

    const svg = d3.select("#" + chart)
        .append('g')
        // .attr("width", width)
        // .attr("height", height)

    // defininf tooltip
    var tooltip = d3.select("body")
        .append("div")
        // .attr("class", "tooltip")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style('font-size', '1em')
        .style("padding", "5px")
        .style('background-color', 'white')
        .style('border-radius', '5px')
        .style("border-width", "2px");

    // reading data directly
    //d3.csv("../../data/participant_scores", function(error, data) {
    d3.csv("/fetchPersonalityScores", function(data) {
        data.forEach(d => {
            d.x = +d.x
            d.y = +d.y
        });

        const participants = Array.from(new Set(data.map(x => x.participantId)).values()).sort();
        selectedParticipantId = participants[Math.floor(Math.random() * participants.length)];    //randomly selecting one of the participants from the list

        // custom shaped for flower glyphs
        //star
        // const customPath = 'M 0,0 C -30,-30 -30,-30 0,-100 C 30,-30 30,-30 0,0'; //normal
        //swrill
        // const customPath = 'M 0,0 C -40,-40 15,-50 50,-100 C 0,-50 0,0 0,0'; //curved thin
        // star1
        // const customPath = 'M 0,0 C -60,-30 0,-40 0,-100 C 0,-40 60,-30 0,0'; //tear drop
        //clover leaf
        // const customPath = "M 0 0 C 50 -80, 80 -100, 0 -100 C -80 -100, -50 -80, 0 0"
        // flower petals
        const customPath = "M 0 0 C 20 -60, 20 -100, 0 -100 C -20 -100, -20 -60, 0 0"

        // var colorInterpolator = d3.quantize(d3.interpolateHcl("#008744", "#d62d20"), 11);
        // var colorInterpolator = d3.quantize(d3.interpolateHcl("orange", "green"), 11);
        // var colorInterpolatorInv = d3.quantize(d3.interpolateHcl("green", "orange"), 11);
        var colorInterpolator = d3.quantize(d3.interpolateRgb("brown", "green"), 11);
        var colorInterpolatorInv = d3.quantize(d3.interpolateRgb("green", "brown"), 11);
        var colorClusters = d3.scaleOrdinal(d3.schemeCategory10);

        // x & y scales for both radial and flower glyphs
        const xScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.x)))
            .range([margin.left + config.r, width - margin.right - config.r])

        const yScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.y)))
            .range([height - margin.bottom - config.r, margin.top + config.r])

        // Scales for radial glyph
        const radialLine = d3.lineRadial()
        const radialScale = d3.scaleLinear()
            .domain([0, 10])
            .range([0, config.r])

        // Add brushing
        var brush = d3.brush() // Add the brush feature using the d3.brush function
            .extent([
                [0, 0],
                [`${margin.left + width + margin.right}`, `${margin.top + height + margin.bottom}`]
            ]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
            .on("end", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

        // Create the svg variable: where both the circles and the brush take place
        // var svg = svg//.append('g')
        // .attr("clip-path", "url(#clip)")

        if (glyph == "radialGlyph") 
        // plotting the radial glyphs
        plotRadialGlyph()

        else if (glyph == "flowerGlyph") 
        // plotting the flower glyphs
        plotFloweGlyph()

        // Add the brushing
        svg
            .append("g")
            .attr("class", "brush")
            .call(brush);

        // A function that set idleTimeOut to null
        var idleTimeout
        function idled() { idleTimeout = null; }

        // adding circles that will help hover and hightlight selected glyphs
        addHoverCircle()

        // adding title
        svg.append("text")
            // .attr("x", -width/5)
            .attr("class", "title")
            .attr("x", width/2 + margin.left    )
            .attr("y", 1.5*margin.top)
            .attr("dy", "-0.1em")
            .style("fill", "rgb(18, 113, 249)")
            .style("font-size", "15px")
            .style("font-weight", "normal")
            .style("text-anchor", "middle")
            .text("Instance View")

        function plotRadialGlyph(){
            // RadialGlyph
            svg.selectAll('circle')
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
                        // .attr('transform', `translate(${(d.x)}, ${(d.y)})`)
                        // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'black')
                        .attr('stroke', d => colorClusters(Math.floor(Math.random() * 2)))
                        .attr('stroke-width', config.strokeWidthHigh * 3)
                        // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'blue')
                        // .attr('fill', d => d.device == "ios" ? "red" : "black") //use this coloring for showing device type ios or android, can also show cluster
                        .attr('fill', d => colorClusters(d.clusters)) //use this coloring for showing device type ios or android, can also show cluster
                        .attr('opacity', config.opacityHigh)
                        // .attr("class", function(d){return d.participantId==selectedParticipantId?"selectedGlyph":""})
                });
                // adding text to show over selected participants
                if (labels == true)
                    addSelectedText()
        }

        function plotFloweGlyph() {
            // flowerGlyph
            svg.selectAll('path')
                .data(data)
                .enter()
                .append('g')
                .each(function(d) {
                    const tPetals = [d.open, d.con, d.extra, d.agree, d.neuro]
                    d3.select(this)
                        .append('g')
                        .selectAll('path')
                        .data(tPetals)
                        .enter()
                        .append('path')
                        .attr('d', function(v) {
                            return customPath
                        })
                        .attr('transform', function(v, i) {
                            return `translate(${xScale(d.x)}, ${yScale(d.y)}), rotate(${360/config.petals * i}), scale(${config.r * v / 1000 })`
                        })
                        .attr("fill", function(v, i) {
                            return i < config.petals ? colorInterpolator[Math.floor(v)] : colorInterpolatorInv[Math.floor(v)]
                        })
                        // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'black')
                        .attr('stroke', 'black')
                        .attr('stroke-width', config.strokeWidthLow)
                        // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participantId) > -1 ? 'red' : 'blue')
                        // .attr('fill', 'none') //use this coloring for showing device type ios or android, can also show cluster
                        .attr('opacity', config.opacityHigh)
                });
                // adding text to show over selected participants
                if (labels == true)
                    addSelectedText()
        }

        function addHoverCircle(){
            // let current_circle = undefined;
            svg.selectAll('.hovercircle')
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'hovercircle')
            .attr("cx", function(d) { return xScale(d.x); })
            .attr("cy", function(d) { return yScale(d.y); })
            .attr("r", config.r)
            .style("fill", config.fillColor)
            .attr('opacity', config.opacityLow)
            .attr('stroke', 'black')
            .attr('stroke-width', config.strokeWidthLow)
            .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px") })
            .on('mouseover', function(d) {
                if (d3.select(this).attr("class") != "hovercircle selectedGlyph")
                    d3.select(this)
                        .attr("opacity", config.opacityHigh)
                        .style('fill', config.fillColorHover)
                        .attr('stroke-width', config.strokeWidthHigh)
                tooltip.text(`${d.participantId} O:${Math.floor(d.open)} C:${Math.floor(d.con)} E:${Math.floor(d.extra)} A:${Math.floor(d.agree)} N:${Math.floor(d.neuro)}`);
                return tooltip.style("visibility", "visible");
            })
            .on('mouseout', function() {
                if (d3.select(this).attr("class") != "hovercircle selectedGlyph"){
                    d3.select(this)
                    .attr("opacity", config.opacityLow)
                    .attr('stroke-width', config.strokeWidthLow)
                    .style("fill", config.fillColor);
                }
                tooltip.style("visibility", "hidden")
            })
            .on("click", function(d) {
                // click on unselected point
                svg.selectAll('.selectedGlyph')
                        .classed('selectedGlyph', false)
                        .attr("opacity", config.opacityLow)
                        .attr("stroke-width", config.strokeWidthLow)
                        .style("fill", config.fillColor);

                if (d3.select(this).attr("class") != "selectedGlyph") {                    
                    d3.select(this).classed('selectedGlyph', true)
                        .attr("opacity", config.opacityHigh)
                        .attr("stroke-width", config.strokeWidthHigh * 2)
                        .style("fill", config.fillColorHover);

                    // click on selected point
                } else if (d3.select(this).attr("class") == "selectedGlyph") {
                    d3.select(this).classed('selectedGlyph', false)
                        .attr("opacity", config.opacityLow)
                        .attr('strokeWidth', config.strokeWidthLow)
                        .style("fill", config.fillColor);
                }

                selectedParticipantId = d.participantId
                // updatePlotAreaChart(dependendChart1, selectedParticipantId, feature, featurelist, brtChecked, accChecked, gyrChecked, lckChecked)
                updateParallelCord(dependendChart2, selectedParticipantId, feature="aggregatedFeatures", featurelist)

                var delayInMilliseconds = 10000; //1 second
                setTimeout(function() {
                    //your code to be executed after 1 second
                    // updateParallelCord(dependendChart3, selectedParticipantId, feature="individualFeatures", featurelist)
                    console.log("have to call the individual cart")
                }, delayInMilliseconds);

                updateParallelCord(dependendChart3, selectedParticipantId, feature="individualFeatures", featurelist)
                return selectedParticipantId
            });
        }

        function addSelectedText(){
            svg.selectAll('text')
                .data(data)
                .enter()
                .append("text")
                .attr("class", "labelText")
                .attr("x", function(d) { return xScale(d.x); })
                .attr("y", function(d) { return yScale(d.y); })
                .attr("dx", (-config.r * 2) + "px")
                .attr("dy", (config.r) + "px")
                .attr("font-size", config.labelSize.toString() + "px")
                .text(function(d) {
                    return d.participantId;
                    // return d.participantId.includes() ? d.participantId : "";
                    // if (["PROSITC0003", "PROSITC0007", "PROSITC0008", "Test"].some(v => d.participantId.includes(v))) {
                    //     return d.participantId
                    // } else { return "" }
                })
        }

        // A function that update the chart for given boundaries
        function updateChart() {
            extent = d3.event.selection
                // If no selection, back to initial coordinate. Otherwise, update X axis domain
            if (!extent) {
                if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
                xScale.domain(d3.extent(data.map(d => d.x)))
                yScale.domain(d3.extent(data.map(d => d.y)))

            } else {
                // svg.selectAll('.glyph').remove();
                xScale.domain([xScale.invert(extent[0][0]), xScale.invert(extent[1][0])])
                yScale.domain([yScale.invert(extent[1][1]), yScale.invert(extent[0][1])])
                tooltip.style("visibility", "hidden")
                svg.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
            }

            // // Update axis and circle position
            // xAxis.transition().duration(1000).call(d3.axisBottom(x))
            svg.selectAll("path").remove()
            svg.selectAll("circle").remove()
            // svg.selectAll("").remove()
            svg.selectAll(".hovercircle").remove()
            svg.selectAll(".labelText").remove()

            if (glyph == "radialGlyph") {
            // plotting the radial glyphs
            plotRadialGlyph()
            }

            else if (glyph == "flowerGlyph") {
            // plotting the flower glyphs
            plotFloweGlyph()
            }

            // // adding circles that will help hover and hightlight selected glyphs
            addHoverCircle()
            
            // // adding text to show over selected participants
            // if (labels == true)
            //         addSelectedText()
        }
    // Plotting chart2 and chart3 with randomly selected participant 
    // updatePlotAreaChart(dependendChart1, selectedParticipantId, feature, featurelist, brtChecked, accChecked, gyrChecked, lckChecked)
    })
}


function updateGlyphs(chart, dependendChart1, dependendChart2, dependendChart3, selectedParticipants, featurelist, radius, glyph, labels, brtChecked, accChecked, gyrChecked, lckChecked) {
    console.log("glyphs called")
    d3.select("#" + chart).selectAll('g').remove();
    d3.select("#" + dependendChart1).selectAll('g').remove();
    glyphs(chart, dependendChart1, dependendChart2, dependendChart3, selectedParticipants, featurelist, radius, glyph, labels, brtChecked, accChecked, gyrChecked, lckChecked)
}