function bubble_chart() {

    // reading the dataset
    data_as_json = d3.csv("https://raw.githubusercontent.com/johnhaldeman/talk-on-d3-basics/master/Summary_sommaire_2017_2026.csv");

    data_as_json.then(data => {
        // let root = { children: data.slice(1) };// remove the first value from the dataset - which is an aggregate we don't need
        // flatNodeHeirarchy = d3.hierarchy(root).sum(d => d.Employment)

        // let width = 930;
        // let height = 930;
        // let pack = d3.pack()
        //     .size([width, height])
        //     .padding(3)
        // packedData = pack(flatNodeHeirarchy);
        // // let width = 932;
        // // let height = 932;

        // const svg = d3.select("#myViz1")//.append(g)
        //     .style("width", "100%")
        //     .style("height", "auto")
        //     .attr("font-size", 10)
        //     .attr("font-family", "sans-serif")
        //     .attr("text-anchor", "middle")

        const inner_svg = d3.select("#myViz1")
            .append("g")

        // .attr("transform", `translate(500, 500)`);

        // const leaf = svg.selectAll("g")
        //     .data(packedData.leaves())
        //     .enter().append("g")
        //     .attr("transform", d => `translate(${d.x + 1},${d.y + 1})`);

        // const circle = leaf.append("circle")
        //     .attr("r", d => d.r)
        //     .attr("fill", d => "#bbccff");




        const data1 = JSON.parse(JSON.stringify(data)).slice(1); // make a copy of the data and then get rid of the first row
        highest_data_as_json = data1.map(d => {
            if (d.Employment_Growth < 0) {
                d.isGrowing = false;
                d.Employment_High = Number(d.Employment);
                d.Employment_Low = Number(d.Employment) + Number(d.Employment_Growth);
            } else {
                d.isGrowing = true;
                d.Employment_High = Number(d.Employment) + Number(d.Employment_Growth);
                d.Employment_Low = Number(d.Employment);
            }

            return d;
        });

        let root = { children: data1.slice(1) }; // remove the first value from the dataset - which is an aggregate we don't need
        flatNodeHeirarchy = d3.hierarchy(root).sum(d => d.Employment)

        let width = 500;
        let height = 500;
        let pack = d3.pack()
            .size([width, height])
            .padding(3)
        packedData = pack(flatNodeHeirarchy);
        // let width = 932;
        // let height = 932;

        // const leaf = svg.selectAll("g")
        //     .data(packedData.leaves())
        //     .enter().append("g")
        //     .attr("transform", d => `translate(${d.x + 1},${d.y + 1})`);

        // let circle = leaf.append("circle")
        //     .attr("r", d => d.r)
        //     .attr("fill", d => {
        //         if (d.data.isGrowing) {
        //             return "#5cb85c";
        //         }
        //         else {
        //             return "#d9534f";
        //         }
        //     });

        // let innerCircles = leaf.append("circle")
        //     .attr("r", d => {
        //         let scale = d3.scaleSqrt()
        //             .domain([0, d.data.Employment_High])  // The employment high
        //             .range([0, d.r]);                      // d.r : radius from packed data (the larger circle)
        //         return scale(d.data.Employment_Low);    // Linearly scaled radius of Employment_Low compares to Employment_High
        //     })
        //     .attr("fill", "#d9edf7");

        // // interactivity to select the circles and change its values 
        // // let format = d3.format(",d")
        // let current_circle = undefined;

        // function selectOccupation(d) {
        //     // cleanup previous selected circle
        //     if (current_circle !== undefined) {
        //         current_circle.attr("fill", d => "#bbccff");
        //         // svg.selectAll("#details-popup").remove();
        //     }
        //     // select the circle
        //     current_circle = d3.select(this);
        //     current_circle.attr("fill", "#000000");

        //     // let textblock = svg.selectAll("#details-popup")
        //     //     .data([d])
        //     //     .enter()
        //     //     .append("g")
        //     //     .attr("id", "details-popup")
        //     //     .attr("font-size", 14)
        //     //     .attr("font-family", "sans-serif")
        //     //     .attr("text-anchor", "start")
        //     //     .attr("transform", d => `translate(0, 20)`);

        //     // textblock.append("text")
        //     //     .text("Occupation Details:")
        //     //     .attr("font-weight", "bold");
        //     // textblock.append("text")
        //     //     .text(d => "Description: " + d.data.Occupation_Name)
        //     //     .attr("y", "16");
        //     // textblock.append("text")
        //     //     .text(d => "Current Employment: " + format(d.data.Employment))
        //     //     .attr("y", "32");
        //     // textblock.append("text")
        //     //     .text(d => "Projected Growth: " + format(d.data.Employment_Growth))
        //     //     .attr("y", "48");
        //     // textblock.append("text")
        //     //     .text(d => "Recent Labour Market Conditions: " + d.data.Recent_Labour_Market_Conditions.toUpperCase())
        //     //     .attr("y", "64");
        //     // textblock.append("text")
        //     //     .text(d => "Projected Future Labour Market Conditionsh: " + d.data.Future_Labour_Market_Conditions.toUpperCase())
        //     //     .attr("y", "80");
        // }

        // circle.on("click", selectOccupation)


        highest_data_grouped_as_json = (function() {
            const data = JSON.parse(JSON.stringify(highest_data_as_json));
            let balance = [];
            let surplus = [];
            let shortage = [];
            let balance_to_surplus = [];
            let balance_to_shortage = [];

            for (let i in data1) {
                let record = data1[i];
                let recent_condititions = record.Recent_Labour_Market_Conditions.toUpperCase();
                let future_condititions = record.Future_Labour_Market_Conditions.toUpperCase();

                if (recent_condititions === "BALANCE" && future_condititions === "BALANCE") {
                    balance.push(record);
                } else if (recent_condititions === "SHORTAGE" && future_condititions === "SHORTAGE") {
                    shortage.push(record);
                } else if (recent_condititions === "SURPLUS" && future_condititions === "SURPLUS") {
                    surplus.push(record);
                } else if (recent_condititions === "BALANCE" && future_condititions === "SHORTAGE") {
                    balance_to_shortage.push(record);
                } else if (recent_condititions === "BALANCE" && future_condititions === "SURPLUS") {
                    balance_to_surplus.push(record);
                }

            }

            return [
                { Description: "Labour Market Outlook Remains Balanced", children: balance },
                { Description: "Labour Market Outlook Remains Shortage", children: shortage },
                { Description: "Labour Market Outlook Remains Surplus", children: surplus },
                { Description: "Labour Market Balanced to Shortage", children: balance_to_shortage },
                { Description: "Labour Market Balanced to Surplus", children: balance_to_surplus },

            ];
        })();

        // Create the heirarchy like we did before, but with the new heirarchical data
        width = 250;
        height = 250;
        pack = d3.pack()
            .size([width, height])
            .padding(3)

        const nodeHeirarchy = d3.hierarchy({
                children: highest_data_grouped_as_json
            })
            .sum(d => d.Employment_High);

        root = pack.padding(7)(nodeHeirarchy)

        const leaf = inner_svg.selectAll("g")
            .data(root.descendants()) // Use descendants() in the join - changed from leaves()
            .enter().append("g")
            .attr("transform", d => `translate(${d.x + 1},${d.y + 1})`);

        const circle = leaf.append("circle")
            .attr("r", d => d.r)
            .attr("fill", d => {
                if (d.height !== 0) { // if you're not a leaf, you don't get a fill
                    return "none";
                } else {
                    if (d.data.isGrowing) {
                        return "#5cb85c";
                    } else {
                        return "#d9534f";
                    }
                }
            });

        let format = d3.format(",d")
        let current_circle = undefined;

        function selectOccupation(d) {
            // cleanup previous selected circle
            if (current_circle !== undefined) {
                // current_circle.attr("fill", d => "#bbccff");
                // current_circle.attr("stroke", d => "#bbccff");
                current_circle.attr("stroke-width", d => "0px");
                // inner_svg.selectAll("#details-popup").remove();
            }

            // select the circle
            current_circle = d3.select(this);
            current_circle.attr("stroke", d => "#000000")
            current_circle.attr("stroke-width", d => "1px");

        }
        circle.on("click", selectOccupation);

    });

}