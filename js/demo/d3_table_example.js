function create_table() {
    let data_as_text = d3.text("https://raw.githubusercontent.com/johnhaldeman/talk-on-d3-basics/master/Summary_sommaire_2017_2026.csv");

    data_as_text.then(function (result) {
        data_as_array = d3.csvParseRows(result);
        let tableObject = d3.select("#mydiv").append("table");
        tableObject.append("tr")         // 1. Append a <tr> element to the table
            .selectAll("th")         // 2. Select all <th> elements in the <tr> (there are none)
            .data(data_as_array[0])  // 3. "Join" that selection to the first row in the CSV data we recieved (an array of string column headers)
            .enter()                 // 4. Perform another selection - getting all elements that do not exist in the table header yet
            .append("th")            // 5. Take this selection (which is all the elements) and append a <th> element
            .text(d => d);           // 6. Put each array element inside the <th> element - creating our column headers

        tableObject.selectAll("tr")
            .data(data_as_array.slice(1, data_as_array.length)) // Join the table rows to the rows in the CSV file (now a js array)
            .enter()
            .append("tr")
            .selectAll("td")
            .data(d => d)                     // Join the table values to the table data
            .enter()
            .append("td")
            .text(d => d);
    })
}