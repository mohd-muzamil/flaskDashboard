// This file is important and I have worked on implementing it for my dummy data

function parallelCord(chart) {
    const svg1 = d3.select("#" + chart)
        .append('g')
        //     .attr("width", width)
        //     .attr("height", height)

    var margin = { left: 10, top: 10, right: 10, bottom: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom,
        innerHeight = height - 2;

    var devicePixelRatio = window.devicePixelRatio || 1;

    var color = d3.scaleOrdinal()
        .domain(["noScreenLocks", "firstScreenUnlock", "lastScreenLock", "maxScreenTime", "totalScreenTime", 
                "noMissed", "noDialled", "noIncoming",  "minDurationIncoming",  "maxDurationIncoming", 
                "totalDurationIncoming", "noOutgoing",  "minDurationOutgoing", "maxDurtaionOutgoing", "totalDurationOutgoing", 
                "totalNoCalls", "totalDurationCalls", "stepCount", "totalDistance" , "noStayPoints", 
                "locationVariance", "locationEntropy", "sleepStartTime1", "sleepEndTime1", "sleepDuration1", 
                "sleepStartTime2", "sleepEndTime2", "sleepDuration2", "totalSleepDuration", "noSleepInterruptions"])
        .range(["#DB7F85", "#50AB84", "#4C6C86", "#C47DCB", "#B59248", 
                "#DD6CA7", "#E15E5A", "#5DA5B3", "#725D82", "#54AF52", 
                "#954D56", "#8C92E8", "#D8597D", "#AB9C27", "#D67D4B", 
                "#D58323", "#BA89AD", "#357468", "#8F86C2", "#7D9E33", 
                "#517C3F", "#9D5130", "#5E9ACF", "#776327", "#944F7E",
                "#517000", "#9D5000", "#5E9000", "#776000", "#944000"]);

    var types = {
        "Number": {
            key: "Number",
            coerce: function(d) { return +d; },
            extent: d3.extent,
            within: function(d, extent, dim) { return extent[0] <= dim.scale(d) && dim.scale(d) <= extent[1]; },
            defaultScale: d3.scaleLinear().range([innerHeight, 0])
        },
        "String": {
            key: "String",
            coerce: String,
            extent: function(data) { return data.sort(); },
            within: function(d, extent, dim) { return extent[0] <= dim.scale(d) && dim.scale(d) <= extent[1]; },
            defaultScale: d3.scalePoint().range([0, innerHeight])
        },
        "Date": {
            key: "Date",
            coerce: function(d) { return new Date(d); },
            extent: d3.extent,
            within: function(d, extent, dim) { return extent[0] <= dim.scale(d) && dim.scale(d) <= extent[1]; },
            defaultScale: d3.scaleTime().range([innerHeight, 0])
        }
    };

    var dimensions = [{
            key: "noScreenLocks",
            description: "No of screen Locks",
            type: types["Number"],
            axis: d3.axisLeft()
                .tickFormat(function(d, i) {
                    return d;
                })
        },
        {
            key: "firstScreenUnlock",
            description: "First screen unlock",
            type: types["Number"]
        },
        {
            key: "lastScreenLock",
            description: "Last Screen lock",
            type: types["Number"]
        },
        {
            key: "maxScreenTime",
            description: "Max screen on time",
            type: types["Number"],
            scale: d3.scaleLog().range([innerHeight, 0])
        },
        {
            key: "totalScreenTime",
            description: "Total screen on time",
            type: types["Number"],
            scale: d3.scaleLog().range([innerHeight, 0])
        },
        {
            key: "noMissed",
            description: "No of missed calls",
            type: types["Number"]
        },
        {
            key: "noDialled",
            description: "No of dialled calls",
            type: types["Number"]
        },
        {
            key: "noIncoming",
            description: "No of incoming calls",
            type: types["Number"]
        },
        {
            key: "minDurationIncoming",
            description: "Smallest incoming call",
            type: types["Number"]
        },
        {
            key: "maxDurationIncoming",
            description: "Largest incoming call",
            type: types["Number"]
        },
        {
            key: "totalDurationIncoming",
            description: "Total duration of incoming calls",
            type: types["Number"]
        },
        {
            key: "noOutgoing",
            description: "No of outgoing calls",
            type: types["Number"]
        },
        {
            key: "minDurationOutgoing",
            description: "Smallest outgoing call",
            type: types["Number"]
        },
        {
            key: "maxDurtaionOutgoing",
            description: "Largest outgoing call",
            type: types["Number"]
        },
        {
            key: "totalDurationOutgoing",
            description: "Total duration of outgoing calls",
            type: types["Number"],
            axis: d3.axisLeft()
                .tickFormat(function(d, i) {
                    if (i % 4) return;
                    return d;
                })
        },
        {
            key: "totalNoCalls",
            description: "Total no of calls",
            type: types["Number"],
        },
        {
            key: "totalDurationCalls",
            description: "Total duration of calls",
            type: types["Number"]
        },
        {
            key: "stepCount",
            description: "No of steps",
            type: types["Number"],
        }
    ];


    var xscale = d3.scalePoint()
        .domain(d3.range(dimensions.length))
        .range([0, width]);

    var yAxis = d3.axisLeft();

    var container = d3.select("#" + chart)
        .append("div")
        .attr("class", "parcoords")
        .style("width", width + margin.left + margin.right + "px")
        .style("height", height + margin.top + margin.bottom + "px");

    var svg = container
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .append("id", "canvas")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var canvas = container.append("canvas")
        .attr("width", width * devicePixelRatio)
        .attr("height", height * devicePixelRatio)
        .style("width", width + "px")
        .style("height", height + "px")
        .style("margin-top", margin.top + "px")
        .style("margin-left", margin.left + "px");
    
    // var canvas = document.getElementById('canvas');

    var ctx = canvas.node().getContext("2d");
    ctx.globalCompositeOperation = 'darken';
    ctx.globalAlpha = 0.15;
    ctx.lineWidth = 1.5;
    ctx.scale(devicePixelRatio, devicePixelRatio);

    var output = d3.select("body").append("pre");

    var axes = svg.selectAll(".axis")
        .data(dimensions)
        .enter().append("g")
        .attr("class", function(d) { return "axis " + d.key.replace(/ /g, "_"); })
        .attr("transform", function(d, i) { return "translate(" + xscale(i) + ")"; });

    d3.csv("../data/dummyFeatureData", function(error, data) {
        if (error) throw error;

        data.forEach(function(d) {
            dimensions.forEach(function(p) {
                d[p.key] = !d[p.key] ? null : p.type.coerce(d[p.key]);
            });

            // truncate long text strings to fit in data table
            for (var key in d) {
                if (d[key] && d[key].length > 35) d[key] = d[key].slice(0, 36);
            }
        });

        // type/dimension default setting happens here
        dimensions.forEach(function(dim) {
            if (!("domain" in dim)) {
                // detect domain using dimension type's extent function
                dim.domain = d3_functor(dim.type.extent)(data.map(function(d) { return d[dim.key]; }));
            }
            if (!("scale" in dim)) {
                // use type's default scale for dimension
                dim.scale = dim.type.defaultScale.copy();
            }
            dim.scale.domain(dim.domain);
        });

        var render = renderQueue(draw).rate(30);

        // ctx.clearRect(0, 0, width, height);
        // ctx.globalAlpha = d3.min([1.15 / Math.pow(data.length, 0.3), 1]);
        // render(data);

        axes.append("g")
            .each(function(d) {
                var renderAxis = "axis" in d ?
                    d.axis.scale(d.scale) // custom axis
                    :
                    yAxis.scale(d.scale); // default axis
                d3.select(this).call(renderAxis);
            })
            .append("text")
            .attr("class", "title")
            .attr("text-anchor", "start")
            .text(function(d) { return "description" in d ? d.description : d.key; });

        // Add and store a brush for each axis.
        axes.append("g")
            .attr("class", "brush")
            .each(function(d) {
                d3.select(this).call(d.brush = d3.brushY()
                    .extent([
                        [-10, 0],
                        [10, height]
                    ])
                    .on("start", brushstart)
                    .on("brush", brush)
                    .on("end", brush)
                )
            })
            .selectAll("rect")
            .attr("x", -8)
            .attr("width", 16);

        d3.selectAll(".axis.pl_discmethod .tick text")
            .style("fill", color);

        output.text(d3.tsvFormat(data.slice(0, 24)));

        function project(d) {
            return dimensions.map(function(p, i) {
                // check if data element has property and contains a value
                if (!(p.key in d) ||
                    d[p.key] === null
                ) return null;

                return [xscale(i), p.scale(d[p.key])];
            });
        };

        function draw(d) {
            ctx.strokeStyle = color(d.pl_discmethod);
            ctx.beginPath();
            var coords = project(d);
            coords.forEach(function(p, i) {
                // this tricky bit avoids rendering null values as 0
                if (p === null) {
                    // this bit renders horizontal lines on the previous/next
                    // dimensions, so that sandwiched null values are visible
                    if (i > 0) {
                        var prev = coords[i - 1];
                        if (prev !== null) {
                            ctx.moveTo(prev[0], prev[1]);
                            ctx.lineTo(prev[0] + 6, prev[1]);
                        }
                    }
                    if (i < coords.length - 1) {
                        var next = coords[i + 1];
                        if (next !== null) {
                            ctx.moveTo(next[0] - 6, next[1]);
                        }
                    }
                    return;
                }

                if (i == 0) {
                    ctx.moveTo(p[0], p[1]);
                    return;
                }

                ctx.lineTo(p[0], p[1]);
            });
            ctx.stroke();
        }

        function brushstart() {
            d3.event.sourceEvent.stopPropagation();
        }

        // Handles a brush event, toggling the display of foreground lines.
        function brush() {
            render.invalidate();

            var actives = [];
            svg.selectAll(".axis .brush")
                .filter(function(d) {
                    return d3.brushSelection(this);
                })
                .each(function(d) {
                    actives.push({
                        dimension: d,
                        extent: d3.brushSelection(this)
                    });
                });

            var selected = data.filter(function(d) {
                if (actives.every(function(active) {
                        var dim = active.dimension;
                        // test if point is within extents for each active brush
                        return dim.type.within(d[dim.key], active.extent, dim);
                    })) {
                    return true;
                }
            });

            // show ticks for active brush dimensions
            // and filter ticks to only those within brush extents
            /*
            svg.selectAll(".axis")
                .filter(function(d) {
                  return actives.indexOf(d) > -1 ? true : false;
                })
                .classed("active", true)
                .each(function(dimension, i) {
                  var extent = extents[i];
                  d3.select(this)
                    .selectAll(".tick text")
                    .style("display", function(d) {
                      var value = dimension.type.coerce(d);
                      return dimension.type.within(value, extent, dimension) ? null : "none";
                    });
                });

            // reset dimensions without active brushes
            svg.selectAll(".axis")
                .filter(function(d) {
                  return actives.indexOf(d) > -1 ? false : true;
                })
                .classed("active", false)
                .selectAll(".tick text")
                  .style("display", null);
            */

            ctx.clearRect(0, 0, width, height);
            ctx.globalAlpha = d3.min([0.85 / Math.pow(selected.length, 0.3), 1]);
            render(selected);

            output.text(d3.tsvFormat(selected.slice(0, 24)));
        }
    });

    function d3_functor(v) {
        return typeof v === "function" ? v : function() { return v; };
    };

}

function updateParallelCord(chart) {
    console.log("parallel cord chart called")
    parallelCord(chart)
}