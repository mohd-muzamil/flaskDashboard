// Warning: The following plot is rather computation intensive, comment it out if you experience lagging.
const glyph_scatter_plot = (chart, dependendChart, radius) => {
    const config = {
        r: +radius,
        opacity: 0.7,
        strokeWidth: 0.5,
    }
    const margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
    // const width = screen.width / 4
    // const height = screen.height / 4
    // const svg = d3.select(DOM.svg(width, height))

    const svg1 = d3.select("#" + chart)
        .append('g')
        //     .attr("width", width)
        //     .attr("height", height)

    const svg2 = d3.select("#" + dependendChart)
        .append('g')

    // tooltip
    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .text("a simple tooltip")
        .style('font-size', '1em')
        .style('background-color', 'white')
        .style('border-radius', '10% 10% 10% 10%');

    // reading data
    d3.csv("../../data/participant_scores", function(error, data) {
        data.forEach(d => {
            d.pca0 = +d.pca0
            d.pca1 = +d.pca1
        });

        const xScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.pca0)))
            .range([margin.left + config.r, width - margin.right - config.r])


        const yScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.pca1)))
            .range([height - margin.bottom - config.r, margin.top + config.r])


        const radialLine = d3.lineRadial()
        const radialScale = d3.scaleLinear()
            .domain([0, 10])
            .range([0, config.r])

        // FlowerGlyph
        svg1.selectAll('circle')
            .data(data)
            .enter()
            // For each Pokemon
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
                    .attr('transform', `translate(${xScale(d.pca0)}, ${yScale(d.pca1)})`)
                    // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'black')
                    .attr('stroke', 'black')
                    .attr('stroke-width', config.strokeWidth)
                    .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'blue')
                    // .attr('fill', 'none') //use this coloring for showing device type ios or android, can also show cluster
                    .attr('opacity', config.opacity)
            });

        let current_circle = undefined;

        svg1.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr("cx", function(d) { return xScale(d.pca0); })
            .attr("cy", function(d) { return yScale(d.pca1); })
            .attr("r", config.r)
            .style("fill", 'white')
            .attr('opacity', 0)

        .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px"); })
            .on('mouseover', function(d) {
                d3.select(this)
                    .attr("opacity", config.opacity)
                    .style("fill", "grey")
                tooltip.text(`O:${Math.floor(d.open)} C:${Math.floor(d.con)} E:${Math.floor(d.extra)} A:${Math.floor(d.agree)} N:${Math.floor(d.neuro)}`);
                return tooltip.style("visibility", "visible");
            })
            .on('mouseout', function() {
                if (d3.select(this).attr("class") != "selectedGlyph")
                    d3.select(this).attr("opacity", 0)
                    .style("fill", "white");
                tooltip.style("visibility", "hidden")

            })
            .on("click", function(d) {
                // click on unselected point
                if (d3.select(this).attr("class") != "selectedGlyph") {
                    svg1.selectAll('.selectedGlyph')
                        .classed('selectedGlyph', false)
                        .attr("opacity", 0)
                        .style("fill", "white");

                    d3.select(this).classed('selectedGlyph', true)
                        .attr("opacity", config.opacity)
                        .style("fill", "grey")
                        .attr("stroke", "black")
                        .attr("stroke-width", config.strokeWidth);

                    // click on selected point
                } else {
                    d3.select(this).classed('selectedGlyph', false);
                    d3.select(this).attr("opacity", 0)
                        .style("fill", "white");
                }
                updateglyph_test(dependendChart, d.participant)

            });

        svg1.selectAll('text')
            .data(data)
            .enter()
            .append("text")
            .attr("x", function(d) { return xScale(d.pca0); })
            .attr("y", function(d) { return yScale(d.pca1); })
            .attr("dx", "-15px")
            .attr("dy", "-10px")
            .attr("font-size", "0.7em")
            .text(function(d) {
                // return d.participant.includes() ? d.participant : "";
                if (["PROSITC0003", "PROSITC0007", "PROSITC0008", "Test"].some(v => d.participant.includes(v))) {
                    return d.participant
                } else { return "" }
            })


    })
}

function updateRadialGlyphs(chart, dependendChart, radius) {
    d3.select("#" + chart).selectAll('g').remove();
    d3.select("#" + dependendChart).selectAll('g').remove();
    glyph_scatter_plot(chart, dependendChart, radius)
}