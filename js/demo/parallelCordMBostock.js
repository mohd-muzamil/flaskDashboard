// d3V4 implementation of code similar to that by Mike Bostock
// https://bl.ocks.org/mbostock/1341021
// https://gist.github.com/kotomiDu/d1fd0fe9397db41f5f8ce1bfb92ad20d

function parallelCord( chart, participantId, feature ){
    // var featuresNames = ["Number of Screen Locks", "first Screen Unlock Event", "last Screen Lock event", "max Screen usage Time", "total Screen usage Time", "no of Missed calls", "no of Dialled calls", "no of Incoming calls", "min Duration of Incoming calls",  "max Duration of Incoming calls", "total Duration of Incoming calls", "no of Outgoing calls",  "min Duration Outgoing calls", "max Durtaion of Outgoing calls", "total Duration Outgoing calls", "total No of Calls", "total Duration of Calls", "step Count", "total Distance travelled" , "no of Stay Points", "location Variance", "location Entropy", "sleep Start Time1", "sleep End Time1", "sleep Duration1", "sleep Start Time2", "sleep End Time2", "sleep Duration2", "total Sleep Duration", "no Sleep Interruptions"],//, "participant"],
    var featuresNames = ["noScreenLocks", "firstScreenUnlock", "lastScreenLock", "maxScreenTime", "totalScreenTime", "noMissed", "noDialled", "noIncoming",  "minDurationIncoming",  "maxDurationIncoming", "totalDurationIncoming", "noOutgoing",  "minDurationOutgoing", "maxDurtaionOutgoing", "totalDurationOutgoing", "totalNoCalls", "totalDurationCalls", "stepCount", "totalDistance" , "noStayPoints", "locationVariance", "locationEntropy", "sleepStartTime1", "sleepEndTime1", "sleepDuration1", "sleepStartTime2", "sleepEndTime2", "sleepDuration2", "totalSleepDuration", "noSleepInterruptions"],
    featuresCodes = ["noScreenLocks", "firstScreenUnlock", "lastScreenLock", "maxScreenTime", "totalScreenTime", "noMissed", "noDialled", "noIncoming",  "minDurationIncoming",  "maxDurationIncoming", "totalDurationIncoming", "noOutgoing",  "minDurationOutgoing", "maxDurtaionOutgoing", "totalDurationOutgoing", "totalNoCalls", "totalDurationCalls", "stepCount", "totalDistance" , "noStayPoints", "locationVariance", "locationEntropy", "sleepStartTime1", "sleepEndTime1", "sleepDuration1", "sleepStartTime2", "sleepEndTime2", "sleepDuration2", "totalSleepDuration", "noSleepInterruptions"];

    var margin = { left: 50, top: 30, right: 50, bottom: 50 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom,
        // deltawidth = width/featuresNames.length;
        line_color = (feature == "aggregatedFeatures") ? "red" : "steelblue";
        deltawidth = width/30;


    // defininf tooltip
    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style('font-size', '1em')
        .style("border-width", "2px")
        .style("padding", "1px")
        .style('background-color', 'white')
        .style('border-radius', '10% 10% 10% 10%');
    
    var x = d3.scalePoint().domain(featuresCodes).range([0, width]),
        y = {};

    var line = d3.line(),
    //        axis = d3.svg.axis().orient("left"),
        background,
        foreground;

    var svg = d3.select( "#" + chart)
        // .attr("width", width + margin.right + margin.bottom)
        // .attr("height", height + margin.top + margin.down)
        .append("svg:g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    postForm = {"participantId": participantId}

    // select server route based on feature paramenter
    if(feature == "aggregatedFeatures"){
        serverRoute = "/fetchAggFeatures"
        titleText = "Aggregated features of all the participants over Study period"
    }
    else if (feature == "individualFeatures"){
        serverRoute = "/fetchIndividualFeatures"
        titleText = "Daily wise features of participant: " + participantId
        // featuresNames.push("date")
        // featuresCodes.push("date")
    }

    d3.csv(serverRoute)
        .header("Content-Type", "application/json")
        .post(JSON.stringify(postForm),
            function(data) {
    // d3.csv("/fetchAggFeatures", function(data) {
        const participants = [...new Set(data.map(item => item.participantId))];

        // Create a scale and brush for each trait.
        featuresCodes.forEach(function(d) {
            // Coerce values to numbers.
            data.forEach(function(p) {p[d] = +p[d]; });

            if( d == "participantId" ) {
                console.log('participantId')
                // y[d] = d3.scaleBand()
                //     .domain(participants)
                //     .range([0, height]);
            }
            else if (d == "date") {
                console.log('date')
            }
            else {
            y[d] = d3.scaleLinear()
                .domain(d3.extent(data, function(p) { return +p[d]; }))
                .range([height, 0]);
            }

            y[d].brush = d3.brushY()
                .extent([[-5, y[d].range()[1]], [5, y[d].range()[0]]]) //刷子范围
                .on("brush", brush);
        });

        // Add a title.
        var title = svg.append("text")
            .attr("x", width/2 )
            .attr("y", -2*margin.top/5)
            .style("font-size", "20px")
            .style("font-weight", "normal")
            .style("text-anchor", "middle")
            .text(titleText)

        // Add a legend.
        var legend = svg.selectAll("g.legend")
                .data(featuresCodes)
                .enter()
                .append("text")
                .style("text-anchor", "middle")
                .style("font-size", "8px")
                // .attr("y", -9)
                .attr("transform", function(d){ return `translate(${x(d)}, ${height + margin.bottom/2}),rotate(-45)`})
                .text(function(d) { return d; });

        var legend = svg.selectAll("g.tootltip")
            .data(featuresNames)
            .enter()
            // .attr('class', "tooltip")
            .append("circle")
            .attr('cx', function(d) { return x(d)} )
            .attr('cy', height + margin.bottom/3)
            .attr('r', deltawidth/2)
            .style('fill', "blue")
            .style("opacity", 0.05)
            .on("mousemove", function() { return tooltip.style("top", (d3.event.pageY + 10 ) + "px").style("left", (d3.event.pageX - 30 ) + "px") })
            .on('mouseover', function(d) {
                console.log("apple", d)
                tooltip.text(d);
                return tooltip.style("visibility", "visible");
            })
            .on('mouseout', function() {
                // d3.select(this).selectAll(".tooltip").remove()
                return tooltip.style("visibility", "hidden");
            })

        legend.append("svg:line")
            .attr("class", String)
            .attr("x2", 8);

        legend.append("svg:text")
            .attr("x", 12)
            .attr("dy", ".31em")
            .text(function(d) { return d; });

        // Add grey background lines for context.
        background = svg.append("svg:g")
            .attr("class", "background")
            .selectAll("path")
            .data(data)
            .enter().append("svg:path")
            .attr("d", path);

        // Add foreground lines.
        foreground = svg.append("svg:g")
            .attr("class", "foreground")
            .selectAll("path")
            .data(data)
            .enter().append("svg:path")
            .attr("d", path)
            // .attr("class", function(d) { return d.featuresNames; });

        // Add a group element for each trait.
        var g = svg.selectAll(".trait")
            .data(featuresCodes)
            .enter().append("svg:g")
            .attr("class", "trait")
            .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
            // .call(d3.drag()
            //     .subject(function(d) { return {x: x(d)}; })
            //     .on("start", dragstart)
            //     .on("drag", drag)
            //     .on("end", dragend));

        // Add an axis and title.
        g.append("svg:g")
            .attr("class", "axis")
            .each(function(d) { d3.select(this).call(d3.axisLeft(y[d])); })
            .append("svg:text")
            .attr("text-anchor", "middle")
            .attr("y", -9)
            .attr("opacity", 0.1)
            .text(String); 

        // Add a brush for each axis.
        g.append("svg:g")
            .attr("class", "brush")
            .each(function(d) { d3.select(this).call(y[d].brush); })
            .selectAll("rect")
            .attr("x", -8)
            .attr("width", 16);
            

    // Returns the path for a given data point.
    function path(d) {
        return line(featuresCodes.map(function(p) { return [x(p), y[p](d[p])]; }));
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

function updateParallelCord(chart, participantId, feature){
    d3.select("#" + chart).selectAll('g').remove();     //clearing the chart before plotting new data
    buffering(chart, participantId);       //calling method that plots buffering symbol
    parallelCord(chart, participantId, feature)
}