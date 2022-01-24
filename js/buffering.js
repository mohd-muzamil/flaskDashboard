function buffering(chart) {
    'use strict';
    var margin = { top: 25, right: 25, bottom: 75, left: 25 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
    var t0 = Date.now();

    // Create svg
    var svg = d3.select('#' + chart);

    var planets = [
        { R: height / 20, r: 10, speed: 50, phi0: 90 }
    ];


    var container = svg.append('g')
        .attr("class", "buffer")
        .attr('transform', `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top/2 + height + margin.bottom) / 2})`);
    // margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom)

    container.append("text")
        .attr("dx", "-4em")
        .attr("dy", "3em")
        .text("Loading Raidal Chart...")

    container.selectAll('g.planet')
        .data(planets)
        .enter().append('g')
        .attr('class', 'planet')
        .each(function(d, i) {
            d3.select(this)
                .append("circle")
                .attr("class", "orbit")
                .attr("r", d.R)
                .style("fill", "none")
                .style("stroke", "black");

            d3.select(this).append('circle')
                .attr('r', d.r)
                .attr('cx', d.R)
                .attr('cy', 0)
                .style("fill", "white")
                // .style("stroke", "black");
        });

    d3.timer(function() {
        var delta = Date.now() - t0;

        svg.selectAll('.planet')
            .attr('transform', function(d) {
                return 'rotate(' + d.phi0 + delta * d.speed / 200 + ')';
            });
    });
}