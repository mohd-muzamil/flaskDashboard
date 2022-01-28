// demo chart to plot a barchar with dummy data
function barchart(chart) {
    var margin = { top: 20, right: 20, bottom: 70, left: 40 },
        width = $("#" + chart).width() - margin.left - margin.right,
        height = $("#" + chart).height() - margin.top - margin.bottom;

    let svg = d3.select("#" + chart),
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    g.append("g")
        .attr("class", "x axis");

    g.append("g")
        .attr("class", "y axis");

    let myData = [
        { name: "John", age: 23, height: 1.93 },
        { name: "Mafe", age: 22, height: 1.70 },
        { name: "Sonia", age: 27, height: 1.60 },
        { name: "Vicente", age: 73, height: 0.32 }
    ];

    let x = d3.scaleBand()
        .padding(0.2)
        .range([0, width]);

    let y = d3.scaleLinear()
        .range([height, 0]);

    function update(myData) {
        x.domain(myData.map(d => d.name));
        y.domain([0, d3.max(myData, d => d.height)]);

        let points = g.selectAll(".point")
            .data(myData); //update

        pointsEnter = points
            .enter()
            .append("rect")
            .attr("class", "point");

        points.merge(pointsEnter) //Enter + Update
            .attr("x", d => x(d.name))
            .attr("y", d => y(d.height))
            .attr("width", d => x.bandwidth())
            .attr("height", d => height - y(d.height))

        .style("fill", "steelblue");

        points.exit()
            .remove();


        g.select(".x.axis")
            .call(d3.axisBottom(x))
            .attr("transform",
                "translate(0, " + height + ")");

        g.select(".y.axis")
            .call(d3.axisLeft(y));
    }


    update(myData);

    // console.log("w", width, " h", height);
}

function updateBarChart(chart) {
    barchart(chart)   
}