function glyph_test(participant) {

    var svg = d3.select("#myViz2").selectAll("g").remove();
    console.log("Chart2 participant: ", participant)
    
    // var chart1 = d3.select("#chart1")
    // chart1.enter()
    // .append("h3")
    // .text("Test")

    opacity = 0.8
    strokewidth = 1

    // Set the dimensions of the canvas / graph
    var margin = { top: 30, right: 10, bottom: 10, left: 20 },
        width = screen.width/4,// - margin.left - margin.right,
        height = screen.height/4;// - margin.top - margin.bottom;

    // Parse the date / time
    var parseDate = d3.timeFormat("%Y-%b-%d");

    // Set the rangeskz
    
    radiusScale = d3.scaleLinear().range([0, width / 2]);
    colorScale = d3.scaleLinear();
    var arcGenerator = d3.arc();

    // Adds the svg canvas
    // var svg = d3.select("#mydiv").append("svg")
    var svg = d3.select("#myViz2")
        .attr("width", width)
        .attr("height", height)
        .append('g');
        // .remove();
        // d3.selectAll("svg > *").remove();

    // Brightness data  Color:Green
    // Get the data
    // d3.csv("../../data/brightness_d3", function (error, data) {
    d3.csv("../../data/accelerometer_d3", function (error, data) {
        data = data.filter(function (row) {
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
          
        data.forEach(function (d) {
            // d.date = parseDate(d.date);
            d.minuteOfTheDay = +d.minuteOfTheDay;
            d.acc = +d.acc;
            // console.log(d)
        });

        // var find_radius = d3.scaleTime()
        //     .domain(d3.extent(data, function(d) { return d.date; }))
        //     .range([50, 200]);

        dates = Array.from(new Set(data.map(x=>x.date)).values()).sort();
        d2i = {};
        dates.forEach((d,i)=>d2i[d]=i);
        console.log(d2i);
        var find_radius = d3.scaleLinear()
            // .domain(d3.extent(data, function(d) { return + (new Date(...d.date.split("-").map((x)=>(+x)))); }))
            .domain([0,dates.length])
            .rangeRound([width/50, width/50 + 100]);

        // console.log(find_radius(data, function(d) { sreturn d.date; }))
        // data.map((d, i) =>{
        //     console.log("radius", find_radius(d.date))
        // });

        slicePerAngle = (2 * Math.PI ) / 1440;
        slices = data.map((d, i) => {
            const my_path = arcGenerator({
                startAngle: d.minuteOfTheDay*slicePerAngle,
                endAngle: (d.minuteOfTheDay+1)*slicePerAngle,
                innerRadius: find_radius(d2i[d.date]),
                outerRadius: find_radius(d2i[d.date]) + d.acc*2 + 0.02//find_radius(d.date)+(d.acc)+0.1
            });

            svg.append("path")
            .attr("d", my_path)
            .attr("fill","blue")
            .attr("transform", `translate(${width/2}, ${height/2})`)
            // .style("stroke", "lightgreen")
            // .style("stroke-width", "10px");

        })

        
        // console.log("COCO", slices)
    })

}
