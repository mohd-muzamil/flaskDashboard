function glyph_test(chart, participant) {
    const config = {
        opacity: 0.8,
        strokewidth: 1
    }

    var svg = d3.select("#" + chart).selectAll("g").remove();
    console.log("Chart2 participant: ", participant)

    // Set the dimensions of the canvas / graph
    var margin = { top: 10, right: 10, bottom: 10, left: 10 },
        width = Math.floor(+$("#" + chart).width()) - margin.left - margin.right,
        height = Math.floor(+$("#" + chart).height()) - margin.top - margin.bottom;

    // Parse the date / time
    var parseDate = d3.timeFormat("%Y-%b-%d");

    // Set the rangeskz

    // radiusScale = d3.scaleLinear().range([0, height / 2]);
    // colorScale = d3.scaleLinear();
    var arcGenerator = d3.arc();

    // Adds the svg canvas
    // var svg = d3.select("#mydiv").append("svg")
    var svg = d3.select("#" + chart)
        .attr("width", width)
        .attr("height", height)
        .append('g');
    // .remove();
    // d3.selectAll("svg > *").remove();

    // Brightness data  Color:Green
    // Get the data
    // d3.csv("../../data/brightness_d3", function (error, data) {
    d3.csv("../../data/accelerometer_d3", function(error, data) {
        data = data.filter(function(row) {
            return row['participant'] == participant //&& row['date'] <= "2020-07-23";// && row['date'] <= "2020-07-23";
        })

        // function isDateInArray(needle, haystack) {
        //     for (var i = 0; i < haystack.length; i++) {
        //       if (needle.getTime() === haystack[i].getTime()) {
        //         return true;
        //       }
        //     }
        //     return false;
        //   }

        //   var dates = [
        //     new Date('October 1, 2016 12:00:00 GMT+0000'),
        //     new Date('October 2, 2016 12:00:00 GMT+0000'),
        //     new Date('October 3, 2016 12:00:00 GMT+0000'),
        //     new Date('October 2, 2016 12:00:00 GMT+0000')
        //   ];

        //   var uniqueDates = [];
        //   for (var i = 0; i < dates.length; i++) {
        //     if (!isDateInArray(dates[i], uniqueDates)) {
        //       uniqueDates.push(dates[i]);
        //     }
        //   }

        data.forEach(function(d) {
            // d.date = parseDate(d.date);
            d.minuteOfTheDay = +d.minuteOfTheDay;
            d.acc = +d.acc;
            // console.log(d)
        });

        // var find_radius = d3.scaleTime()
        //     .domain(d3.extent(data, function(d) { return d.date; }))
        //     .range([50, 200]);

        dates = Array.from(new Set(data.map(x => x.date)).values()).sort();
        d2i = {};
        dates.forEach((d, i) => d2i[d] = i);
        numDates = Object.keys(dates).length
        console.log("Muzzu", d2i.length);
        var find_radius = d3.scaleLinear()
            // .domain(d3.extent(data, function(d) { return + (new Date(...d.date.split("-").map((x)=>(+x)))); }))
            .domain([0, numDates])
            .rangeRound([height / 2 / numDates, height / 2]);

        // console.log(find_radius(data, function(d) { sreturn d.date; }))
        // data.map((d, i) =>{
        //     console.log("radius", find_radius(d.date))
        // });

        slicePerAngle = (2 * Math.PI) / 1440;
        slices = data.map((d, i) => {
            const my_path = arcGenerator({
                startAngle: d.minuteOfTheDay * slicePerAngle,
                endAngle: (d.minuteOfTheDay + 1) * slicePerAngle,
                innerRadius: find_radius(d2i[d.date]),
                outerRadius: find_radius(d2i[d.date]) + d.acc * 2 + 0.02 //find_radius(d.date)+(d.acc)+0.1
            });

            svg.append("path")
                .attr("d", my_path)
                .attr("fill", "blue")
                .attr("transform", `translate(${(margin.left + width + margin.right) / 2}, ${(margin.top + height + margin.bottom) / 2})`)
                // .style("stroke", "lightgreen")
                // .style("stroke-width", "10px");

        })
    })
}