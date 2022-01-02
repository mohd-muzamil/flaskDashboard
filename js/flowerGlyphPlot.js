// Warning: The following plot is rather computation intensive, comment it out if you experience lagging.

const glyph_scatter_plot_copy = (chart, dependendChart, radius) => {
    const config = {
        r: +radius,
        opacity: 0.4,
        strokeWidth: 0.5,
    }



    const margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;
    // const width = screen.width / 4
    // const height = screen.height / 4
    // const svg = d3.select(DOM.svg(width, height))

    const svg1 = d3.select("#" + chart)
        .append('g')
        //     .attr("width", width)
        //     .attr("height", height)

    const svg2 = d3.select("#" + chart)
        .append('g')

    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .text("a simple tooltip")
        .style('font-size', '1em')
        .style('background-color', 'white')
        .style('border-radius', '10% 10% 10% 10%');


    d3.csv("../../data/participant_scores", function(error, data) {
        data.forEach(d => {
            d.pca0 = +d.pca0
            d.pca1 = +d.pca1
        });

        const tPetalPath = 'M 0,0 C -30,-30 -30,-30 0,-100 C 30,-30 30,-30 0,0'; //normal
        const wPetalPath = 'M 0,0 C -40,-40 15,-50 50,-100 C 0,-50 0,0 0,0'; //curved thin
        const pPetalPath = 'M 0,0 C -60,-30 0,-40 0,-100 C 0,-40 60,-30 0,0'; //tear drop
        const customPath = "M 0 0 C 50 80, 80 100, 0 100 C -80 100, -50 80, 0 0"

        const petalSize = 150
            // const height = 1500
            // const width = 1200
        const sideMargin = 300
        const topMargin = 200

        // var colorInterpolator = d3.quantize(d3.interpolateHcl("#008744", "#d62d20"), 11);
        var colorInterpolator = d3.quantize(d3.interpolateHcl("orange", "green"), 11);
        var colorInterpolator1 = d3.quantize(d3.interpolateHcl("green", "orange"), 11);
        // var colorInterpolator1 = d3.interpolateRgb("steelblue", "brown");

        // create a tooltip
        // var tooltip = d3.select("#" + chart)
        //     .append("div")
        //     .style("position", "absolute")
        //     .style("visibility", "hidden")
        //     .text("I'm a glyph!");

        // var tooltip = d3.select("body")
        //     .append("div")
        //     .style("position", "absolute")
        //     .style("z-index", "10")
        //     .style("visibility", "hidden")
        //     // .style("background", "#000")
        //     .text("a simple tooltip");

        // var colScale1 = d3.scaleQuantize().
        // domain([0, 11])
        //     .range(['red', 'green'])

        // var colScale2 = d3.scaleQuantize().
        // domain([0, 11])
        //     .range(['green', 'red'])

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
                    customPath
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



        const flowers = svg1
            .selectAll('g').data(flowersData)
            .enter()
            .append('g')
            .attr('transform', function(d) {
                return `translate(${xScale(d.pca0)}, ${yScale(d.pca1)})`
            }).selectAll("petal")
            .data(function(d) {
                var l = [];
                for (var i = 0; i < 5; i += 1) {
                    var attr = [
                        "openess",
                        "conscientiousness",
                        "extraversion",
                        "agreeableness",
                        "neuroticism"
                    ][i];
                    d.tPetals[i]['personalityTrait'] = attr;
                    d.tPetals[i]['personalityValue'] = d[attr];
                    l.push(d.tPetals[i]);
                }
                return l;
            }).enter().append('path').attr("class", "petal")
            .attr('d', function(d) {
                return d.customPath;
            })
            .attr('transform', function(d) {
                return `translate(0, 0), rotate(${d.angle}), scale(${config.r*d['personalityValue']/1000 })`
            })
            .attr("fill", function(d) {
                return d['personalityTrait'] === "neuroticism" ? colorInterpolator1[Math.floor(d['personalityValue'])] : colorInterpolator[Math.floor(d['personalityValue'])];
            })
            .attr("stroke", "teal")
            .attr("stroke-width", 1)
            .attr("stroke-opacity", 1)
            .attr("opacity", 1);

        svg1.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr("cx", function(d) { return xScale(d.pca0); })
            .attr("cy", function(d) { return yScale(d.pca1); })
            .attr("r", config.r)
            .style("fill", 'grey')
            // .attr('fill', d => ["PROSITC0003", "PROSITC0007", "PROSITC0008"].indexOf(d.participant) > -1 ? 'red' : 'blue')
            .attr('opacity', 0)
            .attr('stroke', 'black')
            .attr('stroke-width', 2)
            .on('mouseover', function(d) {
                var mouse = d3.mouse(this);
                // var xVal = mouse[0];

                // this would work, but not when its called in a function
                // d3.select(this)
                //  .attr('font-size', '2em')

                // this works
                d3.select(this)
                    .attr("opacity", 0.4)
                    .attr('stroke-width', config.strokeWidth * 1.5)
                tooltip.text(`O:${Math.floor(d.open)} C:${Math.floor(d.con)} E:${Math.floor(d.extra)} A:${Math.floor(d.agree)} N:${Math.floor(d.neuro)}`);
                return tooltip.style("visibility", "visible");
                //  .attr('fill', 'red')
            })
            .on('mouseout', function() {
                var mouse = d3.mouse(this);
                // this works
                d3.select(this)
                    .attr("opacity", 0)
                    .attr('stroke-width', 0)
                    //  .attr('fill', 'red')
                tooltip.style("visibility", "hidden")
            })
            .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px"); })
            .on("click", function(d) {
                glyph_test(dependendChart, d.participant)
            });



        svg1.selectAll('text')
            .data(data)
            .enter()
            .append("text")
            .attr("x", function(d) { return xScale(d.pca0); })
            .attr("y", function(d) { return yScale(d.pca1); })
            .attr("dx", "-15px")
            .attr("dy", "-10px")
            .attr("font-size", "0.7em")
            .text(function(d) {
                if (["PROSITC0003", "PROSITC0007", "PROSITC0008", "Test"].some(v => d.participant.includes(v))) {
                    return d.participant
                } else { return "" }
            })
    })
}

function updateFlowerGlyphs(chart, dependendChart, radius) {
    d3.select("#" + chart).selectAll('g').remove();
    d3.select("#" + dependendChart).selectAll('g').remove();
    glyph_scatter_plot_copy(chart, dependendChart, radius)
}