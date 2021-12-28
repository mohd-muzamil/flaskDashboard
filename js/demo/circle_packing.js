var circle_packing = function () {
    // var vWidth = 300;
    // var vHeight = 200;

    // Prepare our physical space
    var g = d3.select('#myViz1')
    const vWidth = Math.floor(g.style("width").replace('px', ''));
    const vHeight = Math.floor(g.style("height").replace('px', ''));

    // var colour = d3.scaleOrdinal(d3.schemeCategory20);

    // Get the data from our CSV file
    d3.csv('../data/data.csv', function (error, vCsvData) {
        if (error) throw error;
        console.log(vCsvData)
        vData = d3.stratify()(vCsvData);
        drawViz(vData);
    });

    function drawViz(vData) {
        // Declare d3 layout
        var vLayout = d3.pack().size([vWidth, vHeight]);

        // Layout + Data
        var vRoot = d3.hierarchy(vData).sum(function (d) { return d.data.size; });
        var vNodes = vRoot.descendants();
        vLayout(vRoot);
        var vSlices = g.selectAll('circle').data(vNodes).enter().append('circle');

        // Draw on screen
        vSlices.attr('cx', function (d) { return d.x; })
            .attr('cy', function (d) { return d.y; })
            .attr('r', function (d) { return d.r; });
        // .style("fill", "Black");

    }

}