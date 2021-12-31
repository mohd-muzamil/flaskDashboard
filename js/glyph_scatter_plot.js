// Warning: The following plot is rather computation intensive, comment it out if you experience lagging.

function glyph_scatter_plot(chart, dependendChart) {
    const config = {
        r: 5,
        opacity: 0.7,
        strokeWidth: 0.5,
    }
    const margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
    // const width = screen.width / 4
    // const height = screen.height / 4
    // const svg = d3.select(DOM.svg(width, height))

    const svg = d3.select("#" + chart)
        //     .attr("width", width)
        //     .attr("height", height)

    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        // .style("background", "#000")
        .text("a simple tooltip");

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





        // .attr('opacity', 0.1)


        svg.selectAll('circle')
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
                        d.neuro,
                        d.open
                    ].map((v, i) => [Math.PI * (i) / 2.5, radialScale(v)])))
                    .attr('transform', `translate(${xScale(d.pca0)}, ${yScale(d.pca1)})`)
                    // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'black')
                    .attr('stroke', 'black')
                    .attr('stroke-width', config.strokeWidth)
                    .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'blue')
                    // .attr('fill', 'none')
                    .attr('opacity', config.opacity)

                // .append("text")
                //     .attr("x", function(d) { return xScale(d.pca0); })
                //     .attr("y", function(d) { return yScale(d.pca1); })
                //     .attr("dx", ".71em")
                //     .attr("dy", ".35em")
                // .text(function(d) { return d.participant;})
                //     // .text(function(d) { return d.participant })
                .on('mouseover', function(d) {
                        var mouse = d3.mouse(this);
                        // var xVal = mouse[0];

                        // this would work, but not when its called in a function
                        // d3.select(this)
                        //  .attr('font-size', '2em')

                        // this works
                        d3.select(this)
                            .attr("opacity", 1)
                            .attr('stroke-width', config.strokeWidth * 1.5)
                            // tooltip.text(d.participant);
                            // return tooltip.style("visibility", "visible");
                            //  .attr('fill', 'red')
                    })
                    .on('mouseout', function() {
                        var mouse = d3.mouse(this);
                        var xVal = mouse[0];

                        // this would work, but not when its called in a function
                        // d3.select(this)
                        //  .attr('font-size', '2em')

                        // this works
                        d3.select(this)
                            .attr("opacity", config.opacity)
                            .attr('stroke-width', config.strokeWidth)
                            //  .attr('fill', 'red')

                        tooltip.style("visibility", "hidden")
                    })
                    .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px"); })
                    .on("click", function(d) {
                        console.log("Chart1 selected participant: ", d.participant);
                        // return d.participant;
                        console.log(dependendChart)
                            // glyph_test(dependendChart, d.participant)

                        glyph(dependendChart)
                        console.log('done')

                    });

            });

        svg.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr("cx", function(d) { return xScale(d.pca0); })
            .attr("cy", function(d) { return yScale(d.pca1); })
            .attr("r", config.r)
            .style("fill", 'none')
            .attr('stroke', 'black')
            .attr('stroke-width', config.strokeWidth / 10);

        svg.selectAll('text')
            .data(data)
            .enter()
            .append("text")
            .attr("x", function(d) { return xScale(d.pca0); })
            .attr("y", function(d) { return yScale(d.pca1); })
            .attr("dx", "-2px")
            .attr("dy", "-10px")
            .attr("font-size", "5px")
            .text(function(d) {
                return d.participant.includes("Test") ? d.participant : d.participant;
            })


    })
}