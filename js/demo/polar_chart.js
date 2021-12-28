function polar_chart() {
    // var colors = ["#d9d9d9", "#ffffb2", "#fecc5c", "#fd8d3c", "#e31a1c"]    //orange yellow
    var colors = ["#000000", "#e41a1c", "#377eb8", "#4daf4a", "#984ea3"] //red blue green
    // var colors = ["#d9d9d9", "#fdd0a2", "#fdae6b", "#f16913", "#d94801", "#7f2704"] //orange yellow red
    // var colors = ["#000000", "#bdbdbd", "#969696", "#525252", "#000000"] //black and white
    num_circles = 30
    dimensions = { width: 1000, height: 1000 }
    myArcGenerator = d3.arc()
        .innerRadius(d => d.radii - 1.3)
        .outerRadius(d => d.radii + 1.3)
        .startAngle(d => d.start)
        .endAngle(d => d.end)
        .cornerRadius(1)

    // myArcGenerator2 = d3.arc()
    //   .innerRadius(d => d.radii +3 - 1)
    //   .outerRadius(d => d.radii +3 + 1)
    //   .startAngle(d => d.start)
    //   .endAngle(d => d.end)
    //   .cornerRadius(1)
    gap = (450 - 100) / num_circles;
    radii = d3.range(450, 100, -gap);
    radii0 = radii.slice(0, radii.length - 1)
    radii1 = radii0.map((r, i) => { return r - 0.25 * gap })
    radii2 = radii0.map((r, i) => { return r - 0.5 * gap })
    radii3 = radii0.map((r, i) => { return r - 0.75 * gap })
    radii4 = radii0.map((r, i) => { return r - gap })

    myAngleScale = d3.scaleLinear().domain([0, 24 * 60 * 60]).range([0, 2 * Math.PI])

    //make a little runif function like R†
    function runif(min, max) {
        // return (Math.random() * (max - min)) + min;
        return (0.5 * (max - min)) + min;
    }

    // rerun this cell to generate new data!
    // data = radii.concat(radii1).concat(radii2).concat(radii3).map((el, i) => {
    data0 = radii.map((el, i) => {
        var start = myAngleScale(runif(0, 24 * 60 * 60));
        return ({
            start: start,
            end: start + myAngleScale(runif(60 * 60, 60 * 60 * 24)),
            radii: el,
            rotation: (i % 2) === 0 ? -1 : 1,
        })
    });

    data1 = radii1.map((el, i) => {
        var start = myAngleScale(runif(0, 24 * 60 * 60 - 1));
        return ({
            start: start,
            end: start + myAngleScale(runif(60 * 60, 60 * 60 * 24)),
            radii: el,
            rotation: (i % 2) === 0 ? -1 : 1,
        })
    });

    data2 = radii2.map((el, i) => {
        var start = myAngleScale(runif(0, 24 * 60 * 60 - 1));
        return ({
            start: start,
            end: start + myAngleScale(runif(60 * 60, 60 * 60 * 24)),
            radii: el,
            rotation: (i % 2) === 0 ? -1 : 1,
        })
    });

    data3 = radii3.map((el, i) => {
        var start = myAngleScale(runif(0, 24 * 60 * 60 - 1));
        return ({
            start: start,
            end: start + myAngleScale(runif(60 * 60, 60 * 60 * 24)),
            radii: el,
            rotation: (i % 2) === 0 ? -1 : 1,
        })
    });

    data4 = radii4.map((el, i) => {
        var start = myAngleScale(runif(0, 24 * 60 * 60 - 1));
        return ({
            start: start,
            end: start + myAngleScale(runif(60 * 60, 60 * 60 * 24)),
            radii: el,
            rotation: (i % 2) === 0 ? -1 : 1,
        })
    });

    var svg = d3.select('#myViz1')
        .attr("viewBox", [0, 0, dimensions.width, dimensions.height])
        .attr("style", "overflow:scroll;")

    radius = 450;
    var ga = svg.append("g")
        .attr("class", "a axis")
        .selectAll("g")
        .data(d3.range(0, 24, 1))
        .enter().append("g")
        // .attr("transform", function (d) { return "rotate(" + -d + ")"; });
        .attr('transform', function (d) { return `translate(500,500)rotate(${-90 + d * 360 / 24})` });// + 'rotate(' + function (d) { return d } + ')');


    ga.append("line")
        .attr("x1", 100 + gap)
        .attr("x2", radius);

    ga.append("text")
        .attr("x", 95)
        .attr("dy", ".35em")
        .style("text-anchor", function (d) { return d < 270 && d > 90 ? "end" : null; })
        .attr("transform", function (d) { return "rotate(45)"; })
        .attr("transform", function (d) { return d < 270 && d > 90 ? "rotate(180 " + (radius + 6) + ",0)" : null; })
        // .text(function (d) { return d + "hrs"; });
        // .text(function (d) { return d == 0 ? "0" : (d == 6 ? "6" : (d == 12 ? "12" : (d == 18 ? "18" : "-"))); });
        .text(function (d) { return d % 6 == 0 ? "x" : "-"; });


    // create circles using each radius.
    svg.selectAll("circle")
        .data(data0)
        .enter().append("circle")
        .attr("fill", "none")
        .attr("stroke", colors[0])
        .attr("r", function (d) { return d.radii })
        .attr('transform', `translate(${dimensions.width / 2}, ${dimensions.height / 2})`)

    // svg.selectAll("circle[name=circle0]")
    //   .enter().append("circle")
    //   .attr("name", "circle0")
    //   .attr("fill", "none")
    //   .attr("stroke", colors[0])
    //   .attr("r", 450)
    //   .attr('transform', `translate(${dimensions.width / 2}, ${dimensions.height / 2})`)


    // now create the paths using our generator
    svg.selectAll("path[name=path1]")
        .data(data1)
        .enter()
        .append("path")
        .attr("name", "path1")
        .attr("class", "arc")
        .attr("d", myArcGenerator)
        .attr("fill", colors[4])
        .attr('transform', function (d, i) {
            // let's leverage Observables generators to rotate our arcs!
            // ...but I am curious how we'd do this without generators - maybe using .transtion()?
            return `translate(${dimensions.width / 2}, ${dimensions.height / 2})`
            // return `translate(${dimensions.width / 2}, ${dimensions.height / 2}) rotate(${rotation * d.rotation + i})`
        })

    svg.selectAll("path[name=path2]")
        .data(data2)
        .enter()
        .append("path")
        .attr("name", "path2")
        .attr("class", "arc")
        .attr("d", myArcGenerator)
        .attr("fill", colors[3])
        .attr('transform', function (d, i) {
            // let's leverage Observables generators to rotate our arcs!
            // ...but I am curious how we'd do this without generators - maybe using .transtion()?
            return `translate(${dimensions.width / 2}, ${dimensions.height / 2})`
            // return `translate(${dimensions.width / 2}, ${dimensions.height / 2}) rotate(${rotation * d.rotation + i})`
        })

    svg.selectAll("path[name=path3]")
        .data(data3)
        .enter()
        .append("path")
        .attr("name", "path3")
        .attr("class", "arc")
        .attr("d", myArcGenerator)
        .attr("fill", colors[2])
        .attr('transform', function (d, i) {
            // let's leverage Observables generators to rotate our arcs!
            // ...but I am curious how we'd do this without generators - maybe using .transtion()?
            return `translate(${dimensions.width / 2}, ${dimensions.height / 2})`
            // return `translate(${dimensions.width / 2}, ${dimensions.height / 2}) rotate(${rotation * d.rotation + i})`
        })

    svg.selectAll("path[name=path4]")
        .data(data4)
        .enter()
        .append("path")
        .attr("name", "path4")
        .attr("class", "arc")
        .attr("d", myArcGenerator)
        .attr("fill", colors[1])
        .attr('transform', function (d, i) {
            // let's leverage Observables generators to rotate our arcs!
            // ...but I am curious how we'd do this without generators - maybe using .transtion()?
            return `translate(${dimensions.width / 2}, ${dimensions.height / 2})`
            // return `translate(${dimensions.width / 2}, ${dimensions.height / 2}) rotate(${rotation * d.rotation + i})`
        })

}