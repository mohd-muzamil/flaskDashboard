// Warning: The following plot is rather computation intensive, comment it out if you experience lagging.

function glyph_scatter_plot() {
  const r = 75
  const width = screen.width/4
  const height = screen.height/4
//   const svg = d3.select(DOM.svg(width, height))
  const svg = d3.select("#myViz1")
  .attr("width", width)
  .attr("height", height)
  
  var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    // .style("background", "#000")
    .text("a simple tooltip");

  const margin = { left: 30, top: 10, right: 10, bottom: 20 }
  


    d3.csv("../../data/participant_scores", function (error, data) {
        data.forEach(d => {
            d.pca0 = +d.pca0
            d.pca1 = +d.pca1
        });

        const xScale = d3.scaleLinear()
        .range([margin.left + r, width - margin.right - r])
        .domain(d3.extent(data.map(d => d.pca0)))
      
      const yScale = d3.scaleLinear()
        .range([height - margin.bottom - r, margin.top + r])
        .domain(d3.extent(data.map(d => d.pca1)))
      
      const radialLine = d3.lineRadial()
      const radialScale = d3.scaleLinear()
        .range([0, r])
        .domain([0, 255])

  svg.selectAll('circle')
    .data(data)
    .enter()
    // For each Pokemon
    .each(function (d) {
      d3.select(this)
        .append('g')
          .selectAll('path')
          .data([d])
          .enter()
          .append('path')
            .attr('d', d => radialLine([
              d.con,
              d.agree,
              d.extra,
              d.neuro,
              d.con
            ].map((v, i) => [Math.PI * i / 3, radialScale(v)])) )
            .attr('transform', `translate(${xScale(d.pca0)}, ${yScale(d.pca1)})`)
            .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'black')
            // .attr('stroke-width', d => d.is_legendary ? 3 : 2)
            // .attr('fill', d => d.is_legendary ? 'DarkGoldenRod' : 'Crimson')
            .attr('opacity', 0.4)
            // .append("text")
            //     .attr("x", function(d) { return xScale(d.pca0); })
            //     .attr("y", function(d) { return yScale(d.pca1); })
            //     .attr("dx", ".71em")
            //     .attr("dy", ".35em")
                // .text(function(d) { return d.participant;})
            //     // .text(function(d) { return d.participant })
            .on('mouseover', function(d) {
                var mouse = d3.mouse(this);
                var xVal = mouse[0];
              
                // this would work, but not when its called in a function
                // d3.select(this)
                //  .attr('font-size', '2em')
              
                // this works
                d3.select(this)
                 .attr("opacity", 1)
                 .attr('stroke-width', 10)
                 tooltip.text(d.participant); return tooltip.style("visibility", "visible");
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
                 .attr("opacity", 0.4)
                 .attr('stroke-width', 1)
                //  .attr('fill', 'red')

                tooltip.style("visibility", "hidden")
            })
      .on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
      .on("click", function(d){
        console.log("Chart1 selected participant: ", d.participant);   
        // return d.participant;
        glyph_test(d.participant)
        // glyph_test()
           
      });

})
})
}