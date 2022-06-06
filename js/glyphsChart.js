// This script is used to generate visual representations over Glyph View.
function glyphs(chart, dependentChart1, dependentChart2, selectedId, featureType, featurelist, classLabel, labels, radius, toggleGlyph, toggleDGrid, toggleLabels, toggleSvgGrid, lckChecked, brtChecked, accChecked, gyrChecked, sleepNoiseChecked) {
    // delta = radius / 100
    const config = {
        r: +radius,
        glyphLegendR: 50,
        opacityLow: 0,
        opacityHigh: 1,
        opacityClickLow: 0.1,
        opacityClickMid: 0.2,
        opacityClickHigh: 0.5,
        // strokeWidthLow: 0.5 - delta,
        // strokeWidthHigh: 2 - delta,
        strokeWidthLow: 0,
        strokeWidthHigh: 1.5,
        fillColor: "transparent",
        fillColorLasso: "#000000",
        petals: featurelist.length, //no of petals in the glyph
        labelSize: radius / 2, //size of labels to show over the glyphs
        toggleBrushOrLasso: "lasso",
        grid_size: 3,
        transition_duration: 750,
        max_zoom: 4,
    }

    if (toggleSvgGrid) { config.opacityLow = 0.2; config.strokeWidthLow = 0.2 }
    const customPath = "M 0 0 C 20 -60, 20 -100, 0 -100 C -20 -100, -20 -60, 0 0" // flower petals
    // const customPath = 'M 0,0 C -30,-30 -30,-30 0,-100 C 30,-30 30,-30 0,0'; //star
    // const customPath = 'M 0,0 C -40,-40 15,-50 50,-100 C 0,-50 0,0 0,0'; //curved thin
    // const customPath = 'M 0,0 C -60,-30 0,-40 0,-100 C 0,-40 60,-30 0,0'; // star1
    // const customPath = "M 0 0 C 50 -80, 80 -100, 0 -100 C -80 -100, -50 -80, 0 0"; //clover leaf
    
    const colorClusters = d3.scaleOrdinal().domain(labels).range(d3.schemeCategory10)
    var current_zoom_scale = 1
    var lassoSelectedIds = []
    var delayInMilliseconds = 750 //1 second
    const titleText = "Glyph View"

    // reading data directly
    d3.csv("/getProjections", function (data) {

        d3.select("#" + chart).selectAll("*").remove()

        const margin = { left: 5, top: 25, right: config.glyphLegendR*2 + config.r, bottom: 5 },
                width = Math.floor(+$("#" + chart).width()),
                height = Math.floor(+$("#" + chart).height())

        const svg = d3.select("#" + chart)
            .style("cursor", "move")

        const svgGlyphs = svg.append("g")
            .style("transform-origin", "0 0 0")

        const svgGrid = svgGlyphs.append("g").attr("class", "grid").lower()

        const svgButtons = svg.append("g").attr("class", "svgButtons").attr("transform", `translate(${margin.left + margin.right - 22},${margin.bottom - 2})`)

        // Add a title.
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", "15px")
            .style("fill", "rgb(18, 113, 249)")
            .style("font-size", "15px")
            .style("font-weight", "normal")
            .style("text-anchor", "middle")
            .text(titleText)
            .lower()

        // rect to assist with zoom and pan
        svgGlyphs.append("rect")
            .attr("class", "rect")
            .attr("width", width)
            .attr("height", height)
            .attr("stroke", "black")
            .attr("stroke-width", "0.1px")
            .attr("fill", "transparent") //rgb(239,239,239)
            .lower()

        // grid
        svgGrid.append("g").attr("class", "vertical")
            .selectAll("line")
            .data(d3.range(0, width, width / 100))
            .enter().append("line")
            .attr("x1", d => { return d })
            .attr("y1", 0)
            .attr("x2", d => { return d })
            .attr("y2", height)
            .style("opacity", (d, i) => {
                return i % Math.ceil(100 / config.grid_size) == 0 ? config.opacityLow * 1.25 : config.opacityLow * 0.6
            })
            .style("stroke", "black")
            .style("stroke-width", config.strokeWidthLow)

        svgGrid.append("g").attr("class", "horizontal")
            .selectAll("line")
            .data(d3.range(0, height, height / 100))
            .enter().append("line")
            .attr("x1", 0)
            .attr("y1", d => { return d })
            .attr("x2", width)
            .attr("y2", d => { return d })
            .style("opacity", (d, i) => {
                return i % Math.ceil(100 / config.grid_size) == 0 ? config.opacityLow * 1.25 : config.opacityLow * 0.6
            })
            .style("stroke", "black")
            .style("stroke-width", config.strokeWidthLow)

        // Legends
        var legendOrdinal = d3.legendColor()
            .title(classLabel.toUpperCase())
            .shapePadding(0)
            .shapeWidth(15)
            .shapeHeight(15)
            .cellFilter(d => { return d.label !== "e" })
            .scale(colorClusters)
            .on("cellover", () => {
                svg.style("cursor", "pointer")
            })
            .on("cellclick", function (e) {
                d3.selectAll(".hovercircle")
                    .classed("selectedLasso", false)
                    .attr("opacity", d => { return d.id == selectedId ? config.opacityHigh : config.opacityLow })
                    .attr("stroke", "black")
                    .attr("stroke-width", d => { return d.id == selectedId ? config.strokeWidthHigh : config.strokeWidthLow })
                    .style("fill", config.fillColor)

                d3.selectAll(".hovercircle")
                    .filter(d => { return d[classLabel] == e })
                    .classed("selectedLasso", true)
                    // .attr("opacity", d => { return (d.id == selectedId ? config.opacityClickHigh :d[classLabel] != d["cluster"]) ? config.opacityClickMid : config.opacityClickLow })
                    .attr("opacity", d => {
                        return (d.id == selectedId) ? config.opacityClickHigh : (d[classLabel] != d["cluster"]) ? config.opacityClickMid : config.opacityClickLow
                    })
                    .attr("stroke", "black")
                    // .attr("stroke-width", d => { return d.id == selectedId ? config.strokeWidthHigh : d[classLabel] != d["cluster"] ? 1*config.strokeWidthLow : config.strokeWidthLow })
                    .attr("stroke-width", d => {
                        return (d.id == selectedId) ? config.strokeWidthHigh : config.strokeWidthHigh / 3
                    })
                    .style("fill", d => {
                        return (d.id == selectedId) ? config.fillColorLasso : config.fillColorLasso
                    })
                callParallelCord()
            })
            .on("cellout", () => {
                svg.style("cursor", "move")
            })
        
        let dwidth = 40
        if(classLabel=="age_group") dwidth = 80
        else if(classLabel=="gender") dwidth = 50
        svg.append("g")
            .attr("class", "legendOrdinal")
            .attr("transform", `translate(${width - dwidth}, ${10}) scale(${1/2})`)
            .call(legendOrdinal)
            .style("opacity", config.opacityHigh)

        var tooltip = d3.select("body")
            .append("div")
            .attr("class", "Tooltip")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("font-size", "12px")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "1px")
            .style("border-radius", "5px")
            .style("padding", "1px")
            .style("pointer-events", "none")
            .style("opacity", 0.8 * config.opacityHigh)

        function tooltip_mousemove(dx = 0, dy = 0) {
            X = d3.event.pageX + dx - 25
            Y = d3.event.pageY + dy + 25
            return tooltip.style("left", X + "px").style("top", Y + "px")
        }

        function tooltip_mouseover(text) {
            if (!d3.event.shiftKey) { svg.style("cursor", "default") }
            tooltip.style("visibility", "visible")
            return tooltip.text(text)
        }

        function tooltip_mouseout() {
            if (!d3.event.shiftKey) { svg.style("cursor", "move") }
            return tooltip.style("visibility", "hidden")
        }

        // zoom code here
        const zoom = d3.zoom().scaleExtent([1, config.max_zoom]).extent([
            [0, 0],
            [width, height]
        ])
            .on("zoom", zoomed)

        svg.call(zoom).on("dblclick.zoom", null)

        d3.select("body")
            .on("keydown", function () {
                if (d3.event.shiftKey) {
                    svg.style("cursor", "crosshair")
                    svg.on(".zoom", null)
                    addLasso()
                }
            })

        d3.select("body").on("keyup", function () {
            svg.style("cursor", "move")
            svg.call(zoom).on("dblclick.zoom", null)
            svgGlyphs.on(".dragstart", null)
            svgGlyphs.on(".drag", null)
            svgGlyphs.on(".dragend", null)
        })

        // x & y scales for both polygon and flower glyphs
        const xScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.x)))
            .range([margin.left + config.r, width - margin.right - config.r])

        const yScale = d3.scaleLinear()
            .domain(d3.extent(data.map(d => d.y)))
            .range([margin.top+config.r, height-margin.bottom-config.r])

        const glyphLegendScale = d3.scaleLinear()
        .domain([0, config.petals])
        .range([0, 360])

        const radians = 0.0174532925,
              labelYOffset = 4;

        // Scales for polygon glyph
        const xpolygonLine = d3.lineRadial()
        const polygonScale = d3.scaleLinear()
            .domain([0, 1])
            .range([0, config.r])

        const polygonScaleConst = d3.scaleLinear()
            .domain([0, 1])
            .range([0, config.glyphLegendR])

        function zoomed(t) {
            // SVG Geometric Zooming
            const transform = d3.event.transform
            svgGlyphs.attr("transform", transform)
        }

        function plotPolygonGlyph(features, legend=false) {
            var featurelistTemp = featurelist.slice()
            featurelistTemp.push(featurelist[0])
            // polygonGlyph
            svgGlyphs.append("g").attr("class", legend === true ? "glyphLegend":"glyphs")
                .selectAll("circle")
                .data(features)
                .enter()
                .each(function (d) {
                    d3.select(this)
                        .append("g")
                        .attr("class", "glyph")
                        .selectAll("path")
                        .data([d])
                        .enter()
                        .append("path")
                        .attr("class", d => { return legend === true ? null : (d.selectedId == selectedId ? "selectedGlyph" : null) })
                        .attr("d", d => {
                            var newPolygonScale = polygonScale
                            if(legend) newPolygonScale = polygonScaleConst
                            return xpolygonLine(featurelistTemp.map(a=>d[a]).map((v, i) => [i* 2*Math.PI / config.petals, newPolygonScale(v)]))
                        })
                        // .attr("d", d => xpolygonLine([d["open"], d["con"], d["extra"], d["agree"], 10 - d["neuro"], d["open"]].map((v, i) => [i* 2*Math.PI / config.petals, polygonScale(v)])))
                        .attr("transform", () => { return toggleDGrid == true ? `translate(${xScale(d.x_overlapRemoved)}, ${yScale(d.y_overlapRemoved)})` : `translate(${xScale(d.x)}, ${yScale(d.y)})` })
                        .attr("opacity", config.opacityHigh)
                        .attr("stroke", colorClusters(d["cluster"]))
                        .attr("stroke-width", config.strokeWidthHigh * 1)
                        .attr("fill", colorClusters(d[classLabel]))
                })
            // adding text to show over selected selectedIds
            if (toggleLabels == true) { addSelectedText() }
        }

        function plotFlowerGlyph(features, legend=false) {
            // flowerGlyph
            svgGlyphs.append("g").attr("class", legend === true ? "glyphLegend":"glyphs")
                .selectAll("path")
                .data(features)
                .enter()
                .append('g')
                .attr("class", d => { return legend === true ? null : (d.selectedId == selectedId ? "selectedGlyph" : null) })
                .each(function (d) {
                    const tPetals = featurelist.map(a=>d[a])
                    d3.select(this)
                        .selectAll("path")
                        .data(tPetals)
                        .enter()
                        .append("path")
                        .attr("d", function (v) {
                            return customPath
                        })
                        .attr("transform", function (v, i) {
                            if(legend) r = config.glyphLegendR
                            else r = config.r
                            translate = toggleDGrid == true ? `translate(${xScale(d.x_overlapRemoved)}, ${yScale(d.y_overlapRemoved)})` : `translate(${xScale(d.x)}, ${yScale(d.y)})`
                            return `${translate}, rotate(${360 / config.petals * i}), scale(${v * r / 100})`
                        })
                        .attr("opacity", config.opacityHigh)
                        .attr("stroke", colorClusters(d["cluster"]))
                        .attr("stroke-width", config.strokeWidthHigh * 5)
                        .attr("fill", colorClusters(d[classLabel]));
                })
            // adding text to show over selected selectedIds
            if (toggleLabels == true) { addSelectedText() }
        }

        function addSelectedText() {
            svgGlyphs.selectAll("text")
                .data(data)
                .enter()
                .append("text")
                .attr("class", "labelText")
                .attr("x", d => { x = toggleDGrid == true ? xScale(d.x_overlapRemoved) : xScale(d.x); 
                return x})
                .attr("y", d => { y = toggleDGrid == true ? yScale(d.y_overlapRemoved) : yScale(d.y) ;
                return y})
                .attr("dx", (-1.5*config.r ) + "px")
                .attr("dy", (1.5*config.r) + "px")
                .attr("font-size", config.labelSize.toString() + "px")
                .attr("opacity", 0.8)
                .text(d => { return d.id })
        }

        function addGlyphLegend(e) {
            d3.selectAll(".glyphLegend").remove()
            var glyphLegend = Object.assign({}, e)
            var dx = width - (config.glyphLegendR + 10)
            var dy = 100 + config.glyphLegendR
            glyphLegend["x"] = xScale.invert(dx)
            glyphLegend["y"] = yScale.invert(dy)
            glyphLegend["x_overlapRemoved"] = glyphLegend["x"]
            glyphLegend["y_overlapRemoved"] = glyphLegend["y"]

            var svgGlyphLegend = svgGlyphs.append("g").attr("class", "glyphLegend").selectAll("glyphLegend")

            svgGlyphLegend.select("circle")
                .data([0])
                .enter()
                .append("circle")
                .attr("cx", dx)
                .attr("cy", dy)
                .attr("r", config.glyphLegendR)
                .attr("opacity", 1/2)
                .attr("stroke", "black")
                .attr("stroke-width", 1/5)
                .style("fill", config.fillColor)

            svgGlyphLegend.select("line")
                .data(d3.range(0, config.petals, 1))
                .enter()
                .append("line")
                .attr("x1", d=>{return dx + config.glyphLegendR * Math.sin(glyphLegendScale(d) * radians)})
                .attr("x2", dx)
                .attr("y1", d=>{return dy - config.glyphLegendR * Math.cos(glyphLegendScale(d) * radians)})
                .attr("y2", dy)
                .attr("opacity", 1/2)
                .attr("stroke", "black")
                .attr("stroke-width", 1 / 5)
                .lower();


            // labels for the glyph legend
            svgGlyphLegend.select("text")
                .data(d3.range(0, config.petals, 1))
                .enter()
                .append('text')
                .attr('text-anchor', 'middle')
                .style('font-size', '10px')
                .style('font-weight', 'lighter')
                .style("cursor", "default")
                .attr("transform", d=>{
                    var x, y
                    x = dx + (config.glyphLegendR + 5) * Math.sin(glyphLegendScale(d) * radians)
                    y = dy - (config.glyphLegendR + 5) * Math.cos(glyphLegendScale(d) * radians) + labelYOffset;
                    return `translate(${x}, ${y}) rotate(0)`
                })
                .text(function(d) {
                    return d+1
                })
                .on("mousemove", () => {
                    tooltip_mousemove()
                })
                .on("mouseover", d => {
                    tooltip_mouseover(((d+1) + ": " + featurelist[d]))
                })
                .on("mouseout", () => {
                    tooltip_mouseout()
                });

            if (toggleGlyph == "polygonGlyph") {
                plotPolygonGlyph(features=[glyphLegend], legend=true)
            } else if (toggleGlyph == "flowerGlyph") {
                plotFlowerGlyph(features=[glyphLegend], legend=true)
            }
        }

        function addHoverCircle(id) {
            // let current_circle = undefined
            svgGlyphs.append("g").attr("class", "hovercircles")
                .selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr("class", d => {return d.id == id ? "hovercircle" : "hovercircle" })
                .attr("cx", d => { return toggleDGrid == true ? xScale(d.x_overlapRemoved) : xScale(d.x) })
                .attr("cy", d => { return toggleDGrid == true ? yScale(d.y_overlapRemoved) : yScale(d.y) })
                .attr("r", config.r)
                .classed("selectedGlyph", d => { return d.id == id ? true : false })
                .attr("opacity", d => { return (d.id == id | d[classLabel] != d["cluster"]) ? config.opacityHigh : config.opacityLow })
                .attr("stroke", "black")
                .attr("stroke-width", d => { return d.id == id ? config.strokeWidthHigh : d[classLabel] != d["cluster"] ? 1*config.strokeWidthLow : config.strokeWidthLow })
                .style("fill", config.fillColor)
                .on("mousemove", () => {
                    tooltip_mousemove()
                })
                .on("mouseover", d => {
                    // tooltip_mousemove()
                    tooltip_mouseover((`id:${d["id"]}`))
                })
                .on("mouseout", () => {
                    tooltip_mouseout()
                })
                .on("click", function (d) {
                    selectedId = d.id
                    classCurrentSelection = d3.select(this).attr("class")
                    // case1: pre-selected lasso-selected
                    if (classCurrentSelection.includes("hovercircle") & classCurrentSelection.includes("selectedGlyph") & classCurrentSelection.includes("selectedLasso")) {
                        // console.log("case1")
                        svgGlyphs.selectAll(".hovercircle")
                            .attr("r", config.r / 2)
                        svgGlyphs.selectAll(".hovercircle")
                            .transition().duration(config.transition_duration)
                            .attr("r", config.r)
                    }
                    // case2: not pre-selected, lasso-selected
                    else if (classCurrentSelection.includes("hovercircle") & classCurrentSelection.includes("selectedLasso")) {
                        // console.log("case2")
                        svgGlyphs.selectAll(".selectedGlyph")
                            .classed("selectedGlyph", false)
                            .attr("opacity", config.opacityLow)
                            .attr("stroke-width", config.strokeWidthLow)
                            .style("fill", config.fillColor)
                        svgGlyphs.selectAll(".selectedLasso")
                            .attr("opacity", config.opacityClickLow)
                            .attr("stroke-width", config.strokeWidthLow)
                            .style("fill", config.fillColorLasso)
                        d3.select(this)
                            .classed("selectedGlyph", true)
                            .attr("opacity", config.opacityClickHigh)
                            .attr("stroke-width", config.strokeWidthHigh)
                            .style("fill", config.fillColorLasso)
                    }
                    // case3: pre-selected not lasso-selected
                    else if (classCurrentSelection.includes("hovercircle") & classCurrentSelection.includes("selectedGlyph")) {
                        // console.log("case3")
                        svgGlyphs.selectAll(".hovercircle")
                            .attr("r", config.r / 2)
                        svgGlyphs.selectAll(".hovercircle")
                            .transition().duration(config.transition_duration)
                            .attr("r", config.r)
                        d3.select(this)
                            .attr("opacity", config.opacityHigh)
                            .attr("stroke-width", config.strokeWidthHigh)
                            .style("fill", config.fillColor)
                    }
                    // case4: not pre-selected, not lasso-selected
                    else if (classCurrentSelection.includes("hovercircle")) {
                        // console.log("case4")
                        svgGlyphs.selectAll(".selectedGlyph")
                            .classed("selectedGlyph", false)
                            .attr("opacity", config.opacityLow)
                            .attr("stroke-width", config.strokeWidthLow)
                            .style("fill", config.fillColor)
                        svgGlyphs.selectAll(".selectedLasso")
                            .attr("opacity", config.opacityClickLow)
                            .attr("stroke-width", config.strokeWidthLow)
                            .style("fill", config.fillColorLasso)
                        d3.select(this)
                            .classed("selectedGlyph", true)
                            .attr("opacity", config.opacityHigh)
                            .attr("stroke-width", config.strokeWidthHigh)
                            .style("fill", config.fillColor)
                    }

                    addGlyphLegend(d)
                    callParallelCord()
                    callRadialTime()
                })
        }

        function addLasso() {
            // ----------------   LASSO STUFF . ----------------
            var lasso_draw = function () {
                svg.style("cursor", "crosshair")
            }

            var lassoEnd = function () {
                lasso.selectedItems() // lasso.notSelectedItems()
                    .classed("selectedLasso", true)
                    .attr("opacity", (d) => {
                        return (d.id == selectedId) ? config.opacityClickHigh : d[classLabel] != d["cluster"] ? config.opacityClickMid : config.opacityClickLow
                    })
                    .attr("stroke", "black")
                    .attr("stroke-width", (d) => {
                        return (d.id == selectedId) ? config.strokeWidthHigh : config.strokeWidthHigh / 3
                    })
                    .style("fill", (d) => {
                        return (d.id == selectedId) ? config.fillColorLasso : config.fillColorLasso
                    })
                if (!d3.event.shiftKey) { svg.style("cursor", "move") }
                callParallelCord()
            }

            circles = svgGlyphs.selectAll(".hovercircle")
            var lasso = d3.lasso()
                .closePathSelect(true)
                .closePathDistance(100)
                .items(circles)
                .targetArea(svgGlyphs)
                // .on("start",lasso_start)
                .on("draw", lasso_draw)
                .on("end", lassoEnd)

            svgGlyphs.call(lasso)
        }


        data.forEach(d => {
            d.x = +d.x
            d.y = +d.y
            d.x_overlapRemoved = +d.x_overlapRemoved
            d.y_overlapRemoved = +d.y_overlapRemoved

            if (d.id == selectedId){
                addGlyphLegend(d)
            }
        })

        if (toggleGlyph == "polygonGlyph") {
            // plotting the polygon glyphs
            plotPolygonGlyph(features=data, legend=false)
        } else if (toggleGlyph == "flowerGlyph") {
            // plotting the flower glyphs
            plotFlowerGlyph(features=data, legend=false)
        }


        addHoverCircle(selectedId)
        // adding text to show over selected selectedIds
        if (toggleLabels) {
            addSelectedText()
        }

        // help button
        svgButtons.append("image")
            .attr("class", "help")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 110 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("xlink:href", "../img/help.png")

        svgButtons.append("rect")
            .attr("class", "help")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 110 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("opacity", config.opacityClickHigh)
            .attr("fill", "transparent")
            .attr("rx", 3)
            .on("mousemove", () => {
                tooltip_mousemove(dx = -50, dy = 0)
            })
            .on("mouseover", d => {
                tooltip_mouseover("Help")
            })
            .on("mouseout", () => {
                tooltip_mouseout()
            })
            .on("click", function () {
                alert(
                    'This is an alert with basic formatting\n\n' +
                    "\t• list item 1\n" +
                    '\t• list item 2\n' +
                    '\t• list item 3\n\n' +
                    '▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬\n\n' +
                    'Simple table\n\n' +
                    'Char\t| Result\n' +
                    '\\n\t| line break\n' +
                    '\\t\t| tab space'
                )
            })

        // clear all button
        svgButtons.append("image")
            .attr("class", "clearall")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 70 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("xlink:href", "../img/clearAll.png")

        svgButtons.append("rect")
            .attr("class", "clearall")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 70 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("opacity", config.opacityClickHigh)
            .attr("stroke", "black")
            .attr("fill", "transparent")
            .attr("rx", 3)
            .on("mousemove", () => {
                tooltip_mousemove(dx = -70, dy = 0)
            })
            .on("mouseover", d => {
                tooltip_mouseover("ClearAll")
            })
            .on("mouseout", () => {
                tooltip_mouseout()
            })
            .on("click", function () {
                d3.select(this).style("fill", "gray")
                d3.select(this).transition().duration(1000).style("fill", "transparent")
                d3.selectAll(".hovercircle")
                    .classed("selectedLasso", false)
                    .attr("opacity", d => { return d.id == selectedId ? config.opacityHigh : config.opacityLow })
                    .attr("stroke", "black")
                    .attr("stroke-width", d => { return d.id == selectedId ? config.strokeWidthHigh : config.strokeWidthLow })
                    .style("fill", config.fillColor)
                callParallelCord()
            })

        // recenter button
        svgButtons.append("image")
            .attr("class", "recenter")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 45 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("xlink:href", "../img/zoomOutMap.png")

        svgButtons.append("rect")
            .attr("class", "recenter")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 45 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("opacity", config.opacityClickHigh)
            .attr("stroke", "black")
            .attr("fill", "transparent")
            .attr("rx", 3)
            .on("mousemove", () => {
                tooltip_mousemove(dx = -80, dy = 0)
            })
            .on("mouseover", d => {
                tooltip_mouseover("Recenter")
            })
            .on("mouseout", () => {
                tooltip_mouseout()
            })
            .on("click", function () {
                d3.select(this).style("fill", "gray")
                d3.select(this).transition().duration(config.transition_duration).style("fill", "transparent")
                svg.transition().duration(config.transition_duration).call(zoom.transform, d3.zoomIdentity)
                svgGlyphs.selectAll(".hovercircle")
                    .attr("r", config.r / 2)
                svgGlyphs.selectAll(".hovercircle")
                    .transition().duration(config.transition_duration)
                    .attr("r", config.r)
            })

        // zoomin button
        svgButtons.append("image")
            .attr("class", "zoomin")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 20 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("xlink:href", "../img/zoomIn.png")

        svgButtons.append("rect")
            .attr("class", "zoomin")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 20 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("opacity", config.opacityClickHigh)
            .attr("stroke", "black")
            .attr("fill", "transparent")
            .attr("rx", 3)
            .on("mousemove", () => {
                tooltip_mousemove(dx = -70, dy = 0)
            })
            .on("mouseover", d => {
                tooltip_mouseover("ZoomIn")
            })
            .on("mouseout", () => {
                tooltip_mouseout()
            })
            .on("click", function () {
                d3.select(this).style("fill", "gray")
                d3.select(this).transition().duration(config.transition_duration).style("fill", "transparent")
                current_zoom_scale = Math.ceil(d3.zoomTransform(svg.node()).k)
                if (current_zoom_scale <= config.max_zoom - 1) {
                    current_zoom_scale += 1
                    svg.transition()
                        .duration(config.transition_duration)
                        .call(zoom.scaleTo, current_zoom_scale)
                } else {
                    svg.transition()
                        .duration(config.transition_duration)
                        .call(zoom.scaleTo, config.max_zoom)
                    svgGlyphs.selectAll(".hovercircle")
                        .attr("r", config.r / 2)
                        .attr("stroke-width", config.strokeWidthHigh / 2)
                    svgGlyphs.selectAll(".hovercircle")
                        .transition().duration(config.transition_duration)
                        .attr("r", config.r)
                        .attr("stroke-width", d => { return d.id == selectedId ? config.strokeWidthHigh : config.strokeWidthLow })
                }
            })

        // zoomout button
        svgButtons.append("image")
            .attr("class", "zoomout")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 0 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("xlink:href", "../img/zoomOut.png")

        svgButtons.append("rect")
            .attr("class", "zoomout")
            .attr("x", width - margin.left - margin.right)
            .attr("y", height - margin.top - 0 - 20)
            .attr("width", 20)
            .attr("height", 20)
            .attr("opacity", config.opacityClickHigh)
            .attr("stroke", "black")
            .attr("fill", "transparent")
            .attr("rx", 3)
            .on("mousemove", () => {
                tooltip_mousemove(dx = -80, dy = 0)
            })
            .on("mouseover", d => {
                tooltip_mouseover("ZoomOut")
            })
            .on("mouseout", () => {
                tooltip_mouseout()
            })
            .on("click", function () {
                d3.select(this).style("fill", "gray")
                d3.select(this).transition().duration(config.transition_duration).style("fill", "transparent")
                current_zoom_scale = Math.floor(d3.zoomTransform(svg.node()).k)
                if (current_zoom_scale > 2) {
                    current_zoom_scale -= 1
                    svg.transition()
                        .duration(config.transition_duration)
                        .call(zoom.scaleTo, current_zoom_scale)
                } else {
                    svg.transition().duration(config.transition_duration).call(zoom.transform, d3.zoomIdentity)
                    svgGlyphs.selectAll(".hovercircle")
                        .attr("r", config.r / 2)
                    svgGlyphs.selectAll(".hovercircle")
                        .transition().duration(config.transition_duration)
                        .attr("r", config.r)
                }
            })
        
        function callRadialTime() {
            updateRadialTime(dependentChart1, dependentChart2, selectedId, featureType, featurelist, classLabel, labels, brtChecked, accChecked, gyrChecked, lckChecked, sleepNoiseChecked)
        }

        function callParallelCord() {
            if ($("#featureType").is(':checked')) {
                featureType = "individualFeatures"
            } else {
                featureType = "aggregatedFeatures"
            }

            lassoSelectedIds = [selectedId]
            d3.selectAll(".selectedLasso")["_groups"][0].forEach(function (d) {
                if (!lassoSelectedIds.includes(d.__data__.id)) { lassoSelectedIds.push(d.__data__.id) }
            })
            lassoSelectedIds = [...new Set(lassoSelectedIds)]
            updateParallelCord(dependentChart2, selectedId, lassoSelectedIds, featureType, featurelist, classLabel, labels, starting_min_date = "", starting_max_date = "")
        }

        d3.select("#" + chart).selectAll('.buffer').remove();
    })
}


function updateGlyphs(chart, dependendChart1, dependendChart2, selectedId, featureType, featurelist, classLabel, labels, radius, toggleGlyph, toggleDGrid, toggleLabels, toggleSvgGrid, lckChecked, brtChecked, accChecked, gyrChecked, sleepNoiseChecked) {
    // only individual parallel cord  will be updated from here.
    glyphs(chart, dependendChart1, dependendChart2, selectedId, featureType, featurelist, classLabel, labels, radius, toggleGlyph, toggleDGrid, toggleLabels, toggleSvgGrid, lckChecked, brtChecked, accChecked, gyrChecked, sleepNoiseChecked)
}