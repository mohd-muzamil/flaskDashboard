function forceSimulation(chart) {
    let svg = d3.select("#" + chart),

        margin = { top: 20, right: 20, bottom: 70, left: 40 },
        width = $("#" + chart).width()/30, //- margin.left - margin.right,
        height = $("#" + chart).height() //- margin.top - margin.bottom,

    svg.attr("width", width)
        .attr("height", height)

    N = 100,
        r = d3.scaleSqrt()
        .domain([0, 50])
        .range([1, 15]),
        x = d3.scaleBand()
        .domain(["M", "F"])
        .range([50, width - 50]),
        c = d3.scaleOrdinal()
        .domain(["M", "F"])
        .range(["steelblue", "firebrick"]),
        y = d3.scaleLinear()
        .domain([20, 50])
        .range([height, 0])

    let nodes = [
        { name: "John", age: 23, gender: "M" },
        { name: "Edwin", age: 25, gender: "M" },
        { name: "Santi", age: 25, gender: "M" },
        { name: "Eliza", age: 22, gender: "F" },
        { name: "Magda", age: 32, gender: "F" },
        { name: "Vicente", age: 43, gender: "M" },
        { name: "Sonia", age: 44, gender: "F" }
    ]

    let links = [
        { source: "John", target: "Vicente", weigth: 3 },
        { source: "Edwin", target: "Vicente" },
        { source: "Santi", target: "Edwin" },
        { source: "Eliza", target: "Vicente" },
        { source: "Magda", target: "Vicente" },
        { source: "John", target: "Sonia" },
        { source: "Edwin", target: "Sonia" },
        { source: "Eliza", target: "Sonia" },

    ]
    console.log(width, height);

    let simulation = d3.forceSimulation(nodes)
        .force("x", d3.forceX((d) => x(d.gender))
            .strength(0.3))
        .force("y", d3.forceY((d) => y(d.age))
            .strength(0.5))
        //     	.force("charge", d3.forceManyBody().strength(-50))
        .force("collide", d3.forceCollide(d => r(d.age) + 1))
        .force("link", d3.forceLink(links)
            .id((d) => d.name)
            .distance(10).strength(0.1))

    .on("tick", ticked);


    console.log("nodes", nodes);
    console.log("links", links);


    let sellinks = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("stroke", "black")
        .attr("stroke-width", d => d.age)
        .attr("fill", "none")
        .style("opacity", 0.9)

    let selnodes = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("class", "node")
        .style("fill", d => c(d.gender))
        .attr("r", d => r(d.age))
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    selnodes.append("title")
        .text(d => d.name);


    function ticked() {
        sellinks.attr("x1", (l) => l.source.x)
            .attr("y1", (l) => l.source.y)
            .attr("x2", (l) => l.target.x)
            .attr("y2", (l) => l.target.y);

        selnodes.attr("cx", (d) => d.x)
            .attr("cy", (d) => d.y);
    } // ticked

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

function updateForceSimulation(chart){
    forceSimulation(chart)
}