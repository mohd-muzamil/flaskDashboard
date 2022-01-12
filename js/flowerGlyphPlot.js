// Warning: The following plot is rather computation intensive, comment it out if you experience lagging.
const flowerGlyph = (chart, dependendChart, radius, brtChecked, accChecked, gyrChecked, lckChecked) => {
    const config = {
        r: +radius,
        opacityLow: 0,
        opacityHigh: 0.8,
        strokeWidthLow: 0,
        strokeWidthHigh: 0.5,
        fillColorHover: "#ddd",
        fillColor: "rgb(255, 255, 255)",
        petals: 5, //no of petals in the glyph
    }
    const margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

    const svg1 = d3.select("#" + chart)
        .append('g')
        //     .attr("width", width)
        //     .attr("height", height)

    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style('font-size', '1em')
        .style('background-color', 'white')
        .style('border-radius', '10% 10% 10% 10%');


    d3.csv("../../data/participant_scores", function(error, data) {
        data.forEach(d => {
            d.x0 = +d.x0
            d.x1 = +d.x1
        });
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
        // var colorInterpolator1 = d3.quantize(d3.interpolateHcl("green", "orange"), 11);
        var colorInterpolator = d3.quantize(d3.interpolateRgb("brown", "green"), 11);
        var colorInterpolator1 = d3.quantize(d3.interpolateRgb("green", "brown"), 11);

        const xScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.x0)))
            .range([margin.left + config.r, width - margin.right - config.r])

        const yScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.x1)))
            .range([height - margin.bottom - config.r, margin.top + config.r])

        // flowerGlyph
        svg1.selectAll('g')
            .data(data)
            .enter()
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
                        return `translate(${xScale(d.x0)}, ${yScale(d.x1)}), rotate(${360/config.petals * i}), scale(${config.r * v / 1000 })`
                    })
                    .attr("fill", function(v, i) {
                        return i < config.petals ? colorInterpolator[Math.floor(v)] : colorInterpolator1[Math.floor(v)]
                    })
                    // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'black')
                    .attr('stroke', 'black')
                    .attr('stroke-width', config.strokeWidthLow)
                    // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'blue')
                    // .attr('fill', 'none') //use this coloring for showing device type ios or android, can also show cluster
                    .attr('opacity', config.opacityHigh)
            });

        svg1.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr("cx", function(d) { return xScale(d.x0); })
            .attr("cy", function(d) { return yScale(d.x1); })
            .attr("r", config.r)
            .style("fill", config.fillColor)
            // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'blue')
            .attr('opacity', config.opacityLow)
            .attr('stroke', 'black')
            .attr('stroke-width', config.strokeWidthLow)
            .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px"); })
            .on('mouseover', function(d) {
                d3.select(this)
                    .attr("opacity", config.opacityHigh)
                    .style('fill', config.fillColorHover)
                    .attr('stroke-width', config.strokeWidthHigh)
                tooltip.text(`O:${Math.floor(d.open)} C:${Math.floor(d.con)} E:${Math.floor(d.extra)} A:${Math.floor(d.agree)} N:${Math.floor(d.neuro)}`);
                return tooltip.style("visibility", "visible");
                //  .attr('fill', 'red')
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
                updateglyph_test(dependendChart, d.participant, brtChecked, accChecked, gyrChecked, lckChecked)
            });



        svg1.selectAll('text')
            .data(data)
            .enter()
            .append("text")
            .attr("x", function(d) { return xScale(d.x0); })
            .attr("y", function(d) { return yScale(d.x1); })
            .attr("dx", "-15px")
            .attr("dy", "-10px")
            .attr("font-size", "0.7em")
            .text(function(d) {
                if (["PROSITC0003", "PROSITC0007", "PROSITC0008", "Test"].some(v => d.participant.includes(v))) {
                    return d.participant
                } else { return "" }
            })
    })
}

function updateFlowerGlyphs(chart, dependendChart, radius, brtChecked, accChecked, gyrChecked, lckChecked) {
    d3.select("#" + chart).selectAll('g').remove();
    d3.select("#" + dependendChart).selectAll('g').remove();
    flowerGlyph(chart, dependendChart, radius, brtChecked, accChecked, gyrChecked, lckChecked)
}