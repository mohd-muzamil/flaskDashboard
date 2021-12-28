var drawGraph_test1 = function(data){
	// var data = [1, 2, 3, 4]

    const width = 300;
	const height = 100;

    numRows = 2;
    numCols = 4;

	//create an svg with width and height
	var svg = d3.select('#myViz1')
		.append('svg')
		.attr("width", width)
		.attr("height", height);
	//x and y axis scales
	var y = d3.scaleBand()
		.range([0, height])
		.domain(d3.range(numRows));

	var x = d3.scaleBand()
		.range([0, width])
		.domain(d3.range(numCols));

	//container to hold the grid
	var container = svg.append("g")
		.attr("transform", "translate(10, 10)");
	
	container.selectAll("circle")
			.data(data)
			.enter().append("circle")
			.attr("id", function(d,i){return "id"+i;})
			.attr('cx', function(d,i){return x(d);})
			.attr('cy', function(d,i){return y(d);})
			.attr('r', 6)
			.attr('fill', function(d,i){return i < Math.floor(count * percentNumber* 0.01) ? twitterFillActive : twitterFill;})
			.style('stroke', 'black')
}

