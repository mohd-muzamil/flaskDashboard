function lineChartData() {
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    radiusScale = d3.scaleLinear().range([0, width / 2]);
    colorScale = d3.scaleLinear();
    arcGenerator = d3.arc();

    // append the svg object to the body of the page
    var svg = d3.select("#myViz1")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/3_TwoNumOrdered_comma.csv", (d) => {
    //     return { date: d3.timeParse("%Y-%m-%d")(d.date), value: d.value }
    // },
    //     (data) => {
    //         plot_cirlce(data)
    //     }
    // )

    // function plot_cirlce(data) {

    //     const perSliceAngle = (2 * Math.PI) / data.length;
    //     const slices = data.map((d, i) => {
    //         var path = arcGenerator({
    //             startAngle: i * perSliceAngle,
    //             endAngle: (i + 1) * perSliceAngle,
    //             innerRadius: radiusScale(d.value),
    //             outerRadius: radiusScale(d.value)
    //         });
    //         return path
    //     });


    // // Read the data
    // d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/3_TwoNumOrdered_comma.csv",

    //     // When reading the csv, I must format variables:
    //     function (d) {
    //         return { date: d3.timeParse("%Y-%m-%d")(d.date), value: d.value }
    //     },

    //     // Now I can use this dataset:
    //     function (data) {

    //         const perSliceAngle = (2 * Math.PI) / data.length;

    //         const slices = data.map((d, i) => {
    //             var path = arcGenerator({
    //                 startAngle: i * perSliceAngle,
    //                 endAngle: (i + 1) * perSliceAngle,
    //                 innerRadius: radiusScale(d.value),
    //                 outerRadius: radiusScale(d.value)
    //             });
    //         });


    //         // // Add X axis --> it is a date format
    //         // var x = d3.scaleTime()
    //         //     .domain(d3.extent(data, function (d) { return d.date; }))
    //         //     .range([0, width]);
    //         // svg.append("g")
    //         //     .attr("transform", "translate(0," + height + ")")
    //         // // .call(d3.axisBottom(x));

    //         // // Add Y axis
    //         // var y = d3.scaleLinear()
    //         //     .domain([0, d3.max(data, function (d) { return +d.value; })])
    //         //     .range([height, 0]);
    //         // svg.append("g")
    //         // // .call(d3.axisLeft(y));
    //         // });
    //         // Add the line
    //         svg.append("path")
    //             .data(slices)
    //             // .attr("fill", "none")
    //             .attr("stroke", "steelblue")
    //             // .attr("stroke-width", 1.5)
    //             .attr("d", d3.line()
    //                 .x(function (d) { return x(d.date) })
    //                 .y(function (d) { return y(d.value) })
    //             )

    //         //     svg.selectAll("path[name=path0]")
    //         //         .data(slices)
    //         //         .enter()
    //         //         .append("path")
    //         //         .attr("name", "path0")
    //         //         .attr("class", "arc")
    //         //         .attr("d", arcGenerator)
    //         //         .attr("fill", "#000000")
    //         //         .attr('transform', function (d, i) {
    //         //             // let's leverage Observables generators to rotate our arcs!
    //         //             // ...but I am curious how we'd do this without generators - maybe using .transtion()?
    //         //             return `translate(${dimensions.width / 2}, ${dimensions.height / 2})`
    //         //             return `translate(${dimensions.width / 2}, ${dimensions.height / 2}) rotate(${rotation * d.rotation + i})`
    //         //         })



    //         // // }

    //         // var arcGen = d3.arc()
    //         //     .innerRadius(0)
    //         //     .outerRadius(90)
    //         //     .startAngle(0)
    //         //     .endAngle(2 * Math.PI);


    //         // d3.select("#myViz1")
    //         //     .append("path")
    //         //     .attr("d", arcGen)
    //         //     .attr("fill", "pink")
    //         //     .attr("stroke", "gray")
    //         //     .attr("stroke-width", 1)
    //         //     .attr("transform", "translate(" + ((width + margin.left + margin.right) / 2) + "," + ((height + margin.top + margin.bottom) / 2) + ")");
    //     });

    //Read the data
    d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/3_TwoNumOrdered_comma.csv",

        // When reading the csv, I must format variables:
        function (d) {
            return { date: d3.timeParse("%Y-%m-%d")(d.date), value: d.value }
        },

        // Now I can use this dataset:
        function (data) {

            // Add X axis --> it is a date format
            var x = d3.scaleTime()
                .domain(d3.extent(data, function (d) { return d.date; }))
                .range([0, width]);
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")

            // Add Y axis
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function (d) { return +d.value; })])
                .range([height, 0]);
            

            data.sort((a, b) => d3.ascending(a.date, b.date));


            // Add the line
            svg.append("g").selectAll("path")
                .data(data)
                .enter()
                .append("path")
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 1.5)
                .attr("r",3)
                .attr('transform', function (d, i) {
                    var r = x(d.date); var theta = y(d.value) / height * 2 * 3.14159;
                    return `translate(${r * Math.cos(theta)}, ${r * Math.sin(theta)})`
                })
        })
}
