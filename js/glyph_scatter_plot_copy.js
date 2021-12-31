// Warning: The following plot is rather computation intensive, comment it out if you experience lagging.

function glyph_scatter_plot_copy(chart, dependendChart) {
    const config = {
        r: 10,
        opacity: 0.7,
        strokeWidth: 1,
    }



    const margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
    // const width = screen.width / 4
    // const height = screen.height / 4
    // const svg = d3.select(DOM.svg(width, height))

    // const svg = d3.select("#" + chart)
    //     .attr("width", width)
    //     .attr("height", height)

    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        // .style("background", "#000")
        .text("a simple tooltip");

    d3.csv("../../data/participant_scores", function(error, data) {
        data.forEach(d => {
            d.pca0 = +d.pca0
            d.pca1 = +d.pca1
        });

        const tPetalPath = 'M 0,0 C -30,-30 -30,-30 0,-100 C 30,-30 30,-30 0,0'; //normal
        const wPetalPath = 'M 0,0 C -40,-40 15,-50 50,-100 C 0,-50 0,0 0,0'; //curved thin
        const pPetalPath = 'M 0,0 C -60,-30 0,-40 0,-100 C 0,-40 60,-30 0,0'; //tear drop

        const petalSize = 150
            // const height = 1500
            // const width = 1200
        const sideMargin = 300
        const topMargin = 200

        // FINDING DOMAIN OF DATA FOR TEMPERATURE, PRECIPITATION, AND WIND SPEED
        // const openess = d3.extent(data, d => d.open);
        // const cons = d3.extent(data, d => d.con);
        // const openess = d3.extent(data, d => d.extra);
        // const openess = d3.extent(data, d => d.agree);
        // const openess = d3.extent(data, d => d.neuro);
        // const tempMinmax = d3.extent(data, d => d.temp.day);
        // const windMinmax = d3.extent(data, d => d.wind_speed);
        // const precipMinmax = d3.extent(data, d => d.rain);

        // DEFINING THE PETAL SCALES
        // const tPetalScAle = d3.scaleQuantize().domain(tempMinmax).range([3, 5, 7, 9, 11, 13]);
        // const wPetalScale = d3.scaleQuantize().domain(windMinmax).range([3, 6, 9, 12, 15, 18]);
        // const pPetalScale = d3.scaleQuantize().domain(precipMinmax).range([3, 4, 5, 6, 7, 8]);

        const flowersData = data.map(function(d) {
            // const tempPetals = tPetalScale(d.temp.day);
            // const windPetals = wPetalScale(d.wind_speed);
            // const precipPetals = pPetalScale(d.rain);
            const Petals = 5
            const petSize = 1

            // const date = new Date(d.dt * 1000).toLocaleDateString("en")
            // const temperature = d.temp.day
            // const windSpeed = d.wind_speed
            // const precip = d.rain

            const openess = d.open
            const conscientiousness = d.con
            const extraversion = d.extra
            const agreeableness = d.agree
            const neuroticism = d.neuro
            const pca0 = d.pca0
            const pca1 = d.pca1

            const tPetals = {}
            for (i = 0; i < Petals; i++) {
                tPetals[i] = {
                    angle: 360 * i / Petals,
                    tPetalPath
                }
            }

            return {
                petSize,
                tPetals,
                // tempPetals,
                // windPetals,
                // precipPetals,
                // date,
                // temperature,
                // windSpeed,
                // precip
                openess,
                conscientiousness,
                extraversion,
                agreeableness,
                neuroticism,
                pca0,
                pca1

            }
        })

        const xScale = d3.scaleLinear()
            .domain(d3.extent(flowersData.map(d => d.pca0)))
            .range([margin.left + config.r, width - margin.right - config.r])


        const yScale = d3.scaleLinear()
            .domain(d3.extent(flowersData.map(d => d.pca1)))
            .range([height - margin.bottom - config.r, margin.top + config.r])


        // const radialLine = d3.lineRadial()
        // const radialScale = d3.scaleLinear()
        //     .domain([0, 10])
        //     .range([0, config.r])

        console.log("Muzzu_data", flowersData)

        const flowers = d3.select("#" + chart)
            .selectAll('g').data(flowersData)
            .enter()
            .append('g')
            .attr('transform', function(d) {
                return `translate(${xScale(d.pca0)}, ${yScale(d.pca1)})`
            }).selectAll("petal")
            .data(function(d) {
                console.log("abc")
                console.log(d.tPetals);
                var l = [];
                for (var i = 0; i < 5; i += 1) {
                    var attr = [
                        "agreeableness",
                        "conscientiousness",
                        "extraversion",
                        "neuroticism",
                        "openess"
                    ][i];
                    d.tPetals[i]["attr"] = d[attr];
                    l.push(d.tPetals[i]);
                }
                console.log(d.tPetals);
                console.log("xyz")
                return l;
            }).enter().append('path').attr("class", "petal")
            .attr('d', function(d) {
                console.log("def");
                console.log(d);
                return d.tPetalPath;
            })
            .attr('transform', function(d) {
                return `rotate(${d.angle}), scale(${0.1*d['attr']/10 })`
            });



        // .append('circle')
        // .attr('r', d => d.openess)
        // .data(d => d.tPetals)
        // .append('path')
        // .attr('d', d => d.tPetals.tPetalPath)
        // .attr('transform', d => `
        // rotate($ { d.angle })
        // `)
        // // .attr('fill', (d, i) => d3.interpolateYlOrRd(d.angle / 360))
        // // .append('path')
        // // .attr('d', wPetalPath)

        // // console.log(d3.select(`#
        // $ { chart }
        // `).selectAll("g"));
        // // flowers.selectAll('.circle1')
        // //     .data(flowersData)
        // //     .enter().append('circle').attr("class", "circle1")
        // //     .attr('r', 5);
        // for (var i = 0; i < 1; i += 1) {
        //     var attr = [
        //         "agreeableness",
        //         "conscientiousness",
        //         "extraversion",
        //         "neuroticism",
        //         "openess"
        //     ][i];
        //     flowers.selectAll(`.path$ { i }
        // `)
        //         .data(flowersData)
        //         .enter().append('path').attr("class", `.path$ { i }
        // `)
        //         .attr('d', d => d.tPetals[i].tPetalPath)
        //         .attr('transform', function(d) {
        //             console.log(0.1 * +d[attr] / 10);
        //             return `
        // rotate($ { d.tPetals[i].angle }), scale($ { 0.1 * +d[attr] / 10 })
        // `
        //         });
        // }

        // .attr('fill', (d, i) => d3.interpolateYlOrRd(d.angle / 360))


        // svg.selectAll('circle')
        //     .data(flowersData)
        //     .enter()
        //     // For each Pokemon
        //     .each(function(d) {
        //         d3.select(this)
        //             .append('g')
        //             .selectAll('path')
        //             .data([d])
        //             .enter()
        //             .append('path')
        //             .attr('d', tPetalPath)
        //             .attr('transform', `
        // translate($ { xScale(d.pca0) }, $ { yScale(d.pca1) }) scale($ { d.open / 100 })
        // `)
        //             // .attr('fill', (d, i) => d3.interpolateYlOrRd(d.open / 360))
        //             // .attr('stroke', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'black')
        //             .attr('stroke', 'black')
        //             .attr('stroke-width', config.strokeWidth)
        //             // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'blue')
        //             .attr('fill', 'none')
        //             .attr('opacity', config.opacity)

        //         // .append("text")
        //         //     .attr("x", function(d) { return xScale(d.pca0); })
        //         //     .attr("y", function(d) { return yScale(d.pca1); })
        //         //     .attr("dx", ".71em")
        //         //     .attr("dy", ".35em")
        //         // .text(function(d) { return d.participant;})
        //         //     // .text(function(d) { return d.participant })
        //         .on('mouseover', function(d) {
        //                 var mouse = d3.mouse(this);
        //                 // var xVal = mouse[0];

        //                 // this would work, but not when its called in a function
        //                 // d3.select(this)
        //                 //  .attr('font-size', '2em')

        //                 // this works
        //                 d3.select(this)
        //                     .attr("opacity", 1)
        //                     .attr('stroke-width', config.strokeWidth * 2)
        //                     // tooltip.text(d.participant);
        //                     // return tooltip.style("visibility", "visible");
        //                     //  .attr('fill', 'red')
        //             })
        //             .on('mouseout', function() {
        //                 var mouse = d3.mouse(this);
        //                 var xVal = mouse[0];

        //                 // this would work, but not when its called in a function
        //                 // d3.select(this)
        //                 //  .attr('font-size', '2em')

        //                 // this works
        //                 d3.select(this)
        //                     .attr("opacity", config.opacity)
        //                     .attr('stroke-width', config.strokeWidth)
        //                     //  .attr('fill', 'red')

        //                 tooltip.style("visibility", "hidden")
        //             })
        //             .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px"); })
        //             .on("click", function(d) {
        //                 console.log("Chart1 selected participant: ", d.participant);
        //                 // return d.participant;
        //                 console.log(dependendChart)
        //                     // glyph_test(dependendChart, d.participant)

        //                 glyph(dependendChart)
        //                 console.log('done')

        // });

        // });

        // svg.selectAll('circle')
        //     .data(data)
        //     .enter()
        //     .append('circle')
        //     .attr("cx", function(d) { return xScale(d.pca0); })
        //     .attr("cy", function(d) { return yScale(d.pca1); })
        //     .attr("r", config.r)
        //     .style("fill", 'none')
        //     .attr('stroke', 'black')
        //     .attr('stroke-width', config.strokeWidth / 10);

        // svg.selectAll('text')
        //     .data(data)
        //     .enter()
        //     .append("text")
        //     .attr("x", function(d) { return xScale(d.pca0); })
        //     .attr("y", function(d) { return yScale(d.pca1); })
        //     .attr("dx", "-2px")
        //     .attr("dy", "-10px")
        //     .attr("font-size", "5px")
        //     .text(function(d) {
        //         return d.participant.includes("Test") ? d.participant : d.participant;
        //     })

    })
}