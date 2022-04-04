/****Importatnt file****/
// This script is used to plot parallel cord charts in third and fourth svg

// d3V4 implementation of code similar to that by Mike Bostock
// https://bl.ocks.org/mbostock/1341021
// https://gist.github.com/kotomiDu/d1fd0fe9397db41f5f8ce1bfb92ad20d
// https://gist.github.com/titipignataro/47135818bad65a439174038227e0eb20


function parallelCord( chart, participantId, feature, featurelist, starting_min_date, starting_max_date ){
    // var featuresNames = ["Number of Screen Locks", "first Screen Unlock Event", "last Screen Lock event", "max Screen usage Time", "total Screen usage Time", "no of Missed calls", "no of Dialled calls", "no of Incoming calls", "min Duration of Incoming calls",  "max Duration of Incoming calls", "total Duration of Incoming calls", "no of Outgoing calls",  "min Duration Outgoing calls", "max Durtaion of Outgoing calls", "total Duration Outgoing calls", "total No of Calls", "total Duration of Calls", "step Count", "total Distance travelled" , "no of Stay Points", "location Variance", "location Entropy", "sleep Start Time1", "sleep End Time1", "sleep Duration1", "sleep Start Time2", "sleep End Time2", "sleep Duration2", "total Sleep Duration", "no Sleep Interruptions"],//, "participantId"],
    // var featuresNames = ["noScreenLocks", "firstScreenUnlock", "lastScreenLock", "maxScreenTime", "totalScreenTime", "noMissed", "noDialled", "noIncoming",  "minDurationIncoming",  "maxDurationIncoming", 
    // "totalDurationIncoming", "noOutgoing",  "minDurationOutgoing", "maxDurtaionOutgoing", "totalDurationOutgoing", "totalNoCalls", "totalDurationCalls", "stepCount", "totalDistance" , "noStayPoints", 
    // "locationVariance", "locationEntropy", "sleepStartTime1", "sleepEndTime1", "sleepDuration1", "sleepStartTime2", "sleepEndTime2", "sleepDuration2", "totalSleepDuration", "noSleepInterruptions"],

    var featuresNames = featurelist 

    if (feature == "aggregatedFeatures"){
        if (featuresNames.includes("date_num")){
            const index = featuresNames.indexOf("date_num");
            if (index > -1) {
            featuresNames.splice(index, 1); // 2nd parameter means remove one item only
            }
        }
    }
    else if  (feature == "individualFeatures"){
        if (!featuresNames.includes("date_num")){
            featuresNames.unshift("date_num")
        }
    }

    var featuresCodes = featuresNames
    var titleText

    var margin = { left: 50, top: 25, right: 20, bottom: 50 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom,
        colorClusters = d3.scaleOrdinal(d3.schemeCategory10),
        line_color = "#1b9e77";  //green
        deltawidth = (width - margin.left - margin.right)/21;

    // defining tooltip
    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style('font-size', '1em')
        .style("border-width", "2px")
        .style("padding", "1px")
        .style('background-color', 'white')
        .style('border-radius', '10% 10% 10% 10%')
        .text("tooltip data");

    var xHigh
    // xHigh = featurelist.length * deltawidth
    
    if(feature == "aggregatedFeatures"){
        featureLength = featurelist.length
    }
    else if (feature == "individualFeatures"){
        featureLength = featurelist.length - 1
    }
    // featureLength = featurelist.length
    if (featureLength<=5){
        // xHigh = featureLength*deltawidth*4
        xHigh = 10 * deltawidth
    }
    else if(featureLength<=10){
        // xHigh = featureLength*deltawidth*2
        xHigh = 15 * deltawidth
    }
    else if(featureLength<=15){
        // xHigh = featureLength*deltawidth*1.3
        xHigh = 20 * deltawidth
    }
    else{
        // xHigh = featureLength*deltawidth
        xHigh = 20 * deltawidth
    }

    if(feature == "aggregatedFeatures"){
        margin.left = margin.left + (20*deltawidth - xHigh)/2 + deltawidth
        // margin.left = margin.left + xHigh/featurelist.length
        }
        else if (feature == "individualFeatures"){
            margin.left = margin.left + (20*deltawidth - xHigh)/2
            xHigh = xHigh + deltawidth
        }
    // margin.left = margin.left + (20*deltawidth - xHigh)/2
    var x = d3.scalePoint().domain(featuresCodes).range([0, xHigh]),
        y = {},
        formatDecimal = d3.format(".0f");

    var line = d3.line(),
        //    axis = d3.svg.axis().orient("left"),
        axis = d3.axisLeft(),
        background,
        foreground;

        dragging = {}

    var svg = d3.select( "#" + chart)
        // .attr("width", width + margin.right + margin.bottom)
        // .attr("height", height + margin.top + margin.down)
        .append("svg:g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    postForm = {"participantId": participantId}

    // select server route based on feature paramenter
    if(feature == "aggregatedFeatures"){
        serverRoute = "/fetchAggFeatures"
        titleText = "Aggregated features of all the participantIds over Study period"
    }
    else if (feature == "individualFeatures"){
        serverRoute = "/fetchIndividualFeatures"
        titleText = "Day-wise features - participantId:" + participantId
        // featuresNames.push("date")
        // featuresCodes.push("date")
    }

    d3.csv(serverRoute)
        .header("Content-Type", "application/json")
        .post(JSON.stringify(postForm),
        function(data) {
        var filteredData = data
        if(feature == "individualFeatures" & (starting_min_date!="" | starting_max_date!="")){ 
            var filteredData = data.filter((d)=>{ 
            if(d.date>=starting_min_date & d.date<=starting_max_date)
                return d
            }   
        )}
        
        // var date_num = [...new Set(filteredData.map(d => d["date_num"]))]
        
        // Create a scale and brush for each trait.
        featuresCodes.forEach(function(d) {
            // Coerce values to numbers.
            
            if( d == "date_num" ) {
                // y[d] = d3.scaleOrdinal()
                //     .domain(date_num)
                //     .range(d3.range(height, 0, -height/date_num.length));
                data.forEach(function(p) { p[d] = formatDecimal(p[d])});
                y[d] = d3.scaleLinear()
                .domain(d3.extent(data, function(p) { return +p[d]; }))
                .range([height, 0])
            }
            // else if (d == "date") {
            //     y[d] = d3.scateTime()
            //         .domain(p[d])
            //         .range([0, height]);
            // }
            else {
            data.forEach(function(p) { p[d] = +p[d]});            
            y[d] = d3.scaleLinear()
                .domain(d3.extent(data, function(p) { return +p[d]; }))
                .range([height, 0]);
            }

            if(true){
            // if (feature == "aggregatedFeatures"){ 
            y[d].brush = d3.brushY()
                .extent([[-7, y[d].range()[1]], [7, y[d].range()[0]]]) //刷子范围
                .on("brush", brush)
                .on("start", brushstart)
                .on("end", brush);
            }
        });


        // Add gray background lines for context.
        background = svg.append("svg:g")
        .attr("class", "background")
        .selectAll("path")
        .data(data)
        .enter().append("svg:path")
        .attr("d", path)
        .attr("stroke", function(d){ 
            return (feature == "aggregatedFeatures") ? colorClusters(d.clusters) : line_color;
        })

        // Add a title.
        var title = svg.append("text")
            .attr("transform", "translate(" + (-margin.left) + "," + 0 + ")")
            .attr("x", width/2 )
            .attr("y", -2*margin.top/5)
            .style("fill", "rgb(18, 113, 249)")
            .style("font-size", "15px")
            .style("font-weight", "normal")
            .style("text-anchor", "middle")
            .text(titleText)

        // Add a legend.
        // var legend = svg.selectAll("g.legend")
        //     .data(featuresNames)
        //     .enter().append("svg:g")
        //     .attr("class", "legend")
        //     // .attr("transform", function(d, i) { return "translate(0," + (i * 20 + 584) + ")"; });
        //     .attr("transform", function(d){ return `translate(${x(d)-deltawidth}, ${height + margin.bottom}),rotate(-45)`});
        
        // legend.append("svg:line")
        //     .attr("class", String)
        //     .attr("x2", 8);
        
        // legend.append("svg:text")
        //     .attr("x", 12)
        //     .attr("dy", ".31em")
        //     .text(function(d) { return d; });

        featureImportanceScale = d3.scaleLinear().domain([0,1])
        .range(["#f0f0f0", "#636363"])

        // add boxes behind each axis 
        var boxes = svg.selectAll("g.tootltip")
        .data(featuresNames)
        .enter()
        .append("rect")
        .attr("class", "boxes")
        .attr("x", function(d) { return x(d) - 2*deltawidth/3} )
        .attr("y", -margin.top * 0.25)
        .attr("width", deltawidth * 0.8)
        .attr("height", height + margin.bottom * 2/3)
        .attr("fill", function(d, i) {return feature == "aggregatedFeatures" ? featureImportanceScale(i/featurelist.length) : "#f0f0f0"})
        .attr("opacity", 0.5)
        // .attr('cx', function(d) { return x(d)} )
        // .attr('cy', height + margin.bottom/3)
        // .attr('r', deltawidth/2)

        // Add foreground lines.
        foreground = svg.append("svg:g")
            .attr("class", "foreground")
            .selectAll("path")
            .data(filteredData)
            .enter().append("svg:path")
            .attr("d", path)
            // .attr("stroke", "red")
            .attr("stroke-width", function(d){
                if(feature == "aggregatedFeatures"){
                    return d.participantId==participantId ? "2px" : "1.5px";
                    }
                    else{
                        return "1.5px"
                    }
            })
            .attr("stroke", function(d){ 
                if(feature == "aggregatedFeatures"){
                    return d.participantId==participantId ? "#252525"  : colorClusters(d.clusters);
                    }
                    else{
                        return line_color
                    }
                
            })
            .attr("opacity", function(d){ 
                if(feature == "aggregatedFeatures"){
                return d.participantId==participantId ? 1 : 0.5;
                }
                else{
                    return 1
                }
            // //     return (feature == "aggregatedFeatures") ? 2 : 1;
            })
            // .attr("class", function(d) { return d.featuresNames; });     can use cluster label to color code the lines
        
        
        // Add a group element for each trait.
        var g = svg.selectAll(".featuresCodes")
            .data(featuresCodes)
            .enter().append("svg:g")
            .attr("class", "featuresCodes")
            .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
            .call(d3.drag()
                .subject(function(d) { return {x: x(d)}; })
                .on("start", function(d) {
                  dragging[d] = x(d);
                  background.attr("visibility", "hidden");
                })
                .on("drag", function(d) {
                  dragging[d] = Math.min(width, Math.max(0, d3.event.x));
                  foreground.attr("d", path);
                  featuresCodes.sort(function(a, b) { return position(a) - position(b); });
                  x.domain(featuresCodes);
                  g.attr("transform", function(d) { return "translate(" + position(d) + ")"; })
                })
                .on("end", function(d) {
                  delete dragging[d];
                  transition(d3.select(this)).attr("transform", "translate(" + x(d) + ")");
                  transition(foreground).attr("d", path);
                  background
                      .attr("d", path)
                      .transition()
                      .delay(500)
                      .duration(0)
                      .attr("visibility", null);
                })
            );
                
       // Add an axis and title.
       g.append("svg:g")
       .attr("class", "axis")
       .each(function(d) { d3.select(this).call(d3.axisLeft(y[d])); })
       .append("svg:text")
       .attr("text-anchor", "middle")
       .attr("y", -0)
       .attr("transform", `translate(${-deltawidth * 0.1}, ${height + margin.bottom * 0.4}) rotate(-45)`)
       .text(function(d){return d})
       .on("mousemove", function(d) { 
        if(d3.event.pageX > 0.95 * width){
            if(d.length<15) return tooltip.style("top", (d3.event.pageY + 1 ) + "px").style("left", (d3.event.pageX - 2*deltawidth ) + "px")
            else return tooltip.style("top", (d3.event.pageY + 1 ) + "px").style("left", (d3.event.pageX - 3.5*deltawidth ) + "px")
        }
        else{return tooltip.style("top", (d3.event.pageY + 1 ) + "px").style("left", (d3.event.pageX - deltawidth) + "px")}
        })
        .on('mouseover', function(d) {
            tooltip.text(d);
            return tooltip.style("visibility", "visible");
        })
        .on('mouseout', function() {
            return tooltip.style("visibility", "hidden");
        }) 

        //     .on("mousemove", function() { 
        //         if(d3.event.pageX < 0.95*width){return tooltip.style("top", (d3.event.pageY + 10 ) + "px").style("left", (d3.event.pageX - deltawidth ) + "px")}
        //         else{return tooltip.style("top", (d3.event.pageY + 10 ) + "px").style("left", (d3.event.pageX - 3*deltawidth) + "px")}
        //     })
        //     .on('mouseover', function(d) {x
        //         tooltip.text(d);
        //         return tooltip.style("visibility", "visible");
        //     })
        //     .on('mouseout', function() {
        //         // d3.select(this).selectAll(".tooltip").remove()
        //         return tooltip.style("visibility", "hidden");
        //     })
        
        
        
        if (feature == "aggregatedFeatures"){ 
        // Add a brush for each axis.
        g.append("svg:g")
            .attr("class", "brush")
            .each(function(d) { d3.select(this).call(y[d].brush); })
            .selectAll("rect")
            .attr("x", -8)
            .attr("width", 16);
        }

        function position(d) {
            var v = dragging[d];
            return v == null ? x(d) : v;
        }
        function transition(g) {
            return g.transition().duration(500);``
        }
        // Returns the path for a given data point.
        function path(d) {
            return line(featuresCodes.map(function(p) { 
                return [position(p), y[p](d[p])]; }));
        }

        function dragstart(d) {
            i = featuresCodes.indexOf(d);
        }

        function drag(d) {
            x.range()[i] = d3.event.x; //unsovled issue
            featuresCodes.sort(function(a, b) { return x(a) - x(b); });
            g.attr("transform", function(d) { return "translate(" + x(d) + ")"; });
            foreground.attr("d", path);
        }

        function dragend(d) {
            //x.domain(featuresCodes).rangePoints([0, w]);
            var t = d3.transition().duration(500);
            t.selectAll(".trait").attr("transform", function(d) { return "translate(" + x(d) + ")"; });
            t.selectAll(".foreground path").attr("d", path);
        }


        function brushstart() {
            d3.event.sourceEvent.stopPropagation();
        }
        // Handles a brush event, toggling the display of foreground lines.
        function brush() {
            var actives = [];
            //filter brushed extents
            svg.selectAll(".brush")
                .filter(function(d) {
                    return d3.brushSelection(this);
                })
                .each(function(d) {
                    actives.push({
                        dimension: d,
                        extent: d3.brushSelection(this)
                    });
                });

            //set un-brushed foreground line disappear
            foreground.classed("fade", function(d,i) {
                return !actives.every(function(active) {
                    var dim = active.dimension;
                    return active.extent[0] <= y[dim](d[dim]) && y[dim](d[dim])  <= active.extent[1];
                });
            });
            
        }
    d3.select("#" + chart).selectAll('.buffer').remove();
    });
}

function updateParallelCord(chart, participantId, feature, featurelist, starting_min_date="", starting_max_date=""){   
    if(Array.isArray(participantId)){
        participantId = participantId[0]
    }
    // d3.select("#" + chart).selectAll('*').remove();     //clearing the chart before plotting new data
    d3.select("#" + chart).selectAll("*").remove();
    // d3.select("#" + chart).remove();     //clearing the chart before plotting new data
    buffering(chart, participantId);       //calling method that plots buffering symbol
    parallelCord(chart, participantId, feature, featurelist, starting_min_date, starting_max_date)
}