var drawGraph_test = function(data) {

    //number of circles to color in to visualize percent
    var selections = [];
    var count = 4 //data.length
    var percentNumber = 75;

    //variables for the font family, and some colors
    var fontFamily = "helvetica";
    var twitterFill = "#ff5733";
    var twitterFillActive = "#adf7b6";
    var svgBackgroundColor = '#264653';


    //create an svg with width and height
    var svg = d3.select('#chart3')
    const width = Math.floor(svg.style("width").replace('px', ''));
    const height = Math.floor(svg.style("height").replace('px', ''));

    //radius of circles
    // r = Math.sqrt(width * height / Math.PI / count / 2)
    r = Math.floor(Math.sqrt(Math.floor(width * height / count)) / 2) - 3

    svg.append('svg')
        .attr("width", width)
        .attr("height", height)
        .style('background-color', svgBackgroundColor);

    //rows and columns for the grid
    var numRows = Math.floor(height / (2.5 * r));
    var numCols = Math.floor(width / (2.5 * r));

    //x and y axis scales
    var y = d3.scaleBand()
        .range([0, height])
        .domain(d3.range(numRows));

    var x = d3.scaleBand()
        .range([0, width])
        .domain(d3.range(numCols));

    //the data is just an array of numbers for each cell in the grid
    // var data = d3.range(count);
    var data = data;

    //container to hold the grid
    var container = svg.append("g")
        .attr("transform", "translate(" + 1.1 * r + "," + 1.1 * r + ")");
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    container.exit().remove();

    container.selectAll("circle")
        .data(data)
        .enter().append("circle")
        .attr("id", function(d, i) { return "id" + i; })
        .attr('cx', function(d, i) { return x(i % numCols); })
        .attr('cy', function(d, i) { return y(Math.floor(i / numCols)); })
        .attr('r', r)
        // .attr('fill', function(d,i){return i < Math.floor(count * percentNumber* 0.01) ? twitterFillActive : twitterFill;})
        // .style('stroke', 'black')
        // .style("stroke-opacity", .2)
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", 1);
            div
                .html(d + "<br/>")
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .on("click", function(d) {
            var participant
            if (!d3.select(this).classed("selected")) {
                d3.selectAll("circle").attr("r", r).attr("stroke", "none");
                d3.select(this).classed("selected", true);
                d3.select(this).attr("r", r + 3).attr("stroke", "red").attr("stroke-width", "2");
                participant = d;
                fetch_data(participant)
                console.log("participant", participant)
                    // console.log('classed now', d3.select(this).classed("selected"), d)
                    //call a routine to fetch data from db and make a chart that goes in myViz2, myViz3.
            } else {
                if (d3.select(this).classed("selected") == false) {
                    d3.select(this).classed("selected", true);
                    d3.select(this).attr("r", r + 3).attr("stroke", "red").attr("stroke-width", "2");
                    // participant = d;
                    fetch_data(participant)
                        // console.log("participant", participant)
                        // console.log('classed', d3.select(this).classed("selected"), d)
                        //call a routine to fetch data from db and make a chart that goes in myViz2, myViz3.
                } else if (d3.select(this).classed("selected") == true) {
                    d3.select(this).classed("selected", false);
                    d3.select(this).attr("r", r).attr("stroke", "none");
                    // console.log('unclassed', d3.select(this).classed("selected"), d)
                    //delete visualizations in myViz2, myViz3 since nothing has been selected yet.
                }
            }



        });
    // (update) => {},
    // (exit) => {}

    // function to fetch the Accelerometer data from the database.
    function fetch_data(participant) {
        $.ajax({
            url: '/fetch_data',
            type: 'POST',
            data: { "participantId": participant, attribute: "Brightness" },
            dataType: 'json', //make sure your service is actually returning json here
            success: function(data) {
                // data.forEach(function(d) {
                // console.log("Jeni", d)
                // var count = data.length;
                // console.log("jenu", count)
                console.log("coco", data)
            }
        });
    };


};


//code for multiple circle selection on mouse clicks:
// .on("click", function(d) {
// 	if (!d3.select(this).classed("selected") )
// 		{
// 		d3.select(this).classed("selected", true);
// 		d3.select(this).attr("r", r+1).attr("stroke-width", 2);
// 		selections.push(d);
// 		} 

// 	else{
// 		if (d3.select(this).classed("selected", true)) {
// 			d3.select(this).classed("selected", false);
// 			d3.select(this).attr("r", r).attr("stroke-width",1)

// 			if (selections.includes(d)) {
// 				const index = selections.indexOf(d);
// 					if (index > -1) {
// 						selections.splice(index, 1);
// 					}
// 				}
// 			}
// 		else if (d3.select(this).classed("selected", false)) {
// 			d3.select(this).classed("selected", true);
// 			d3.select(this).attr("r", 8).attr("stroke-width", 2)
// 			selections.push(d);		
// 			}
// 		}

// })