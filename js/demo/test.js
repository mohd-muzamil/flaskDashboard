var test = function() {
    // function to test the creation of the data needed to make the circle packing chart.

    function fetch_data(participant) {
        console.log("printing from here", participant);
        $.ajax({
            url: '/fetch_data',
            type: 'POST',
            data :{"participantId":participant, attribute:"Brightness"},
            dataType: 'json', //make sure your service is actually returning json here
            success: function (data) {
                // data.forEach(function(d) {
                // console.log("Jeni", d)
                // var count = data.length;
                // console.log("jenu", count)
                console.log("coco", data)
                },
                error: function (errorMessage) { // error callback 
                    console.log("error", errorMessage)
                }
            });
            console.log("end");
        };


	function fetch_participants() {
		$.ajax({
			url: '/participants',
			type: 'POST',
			dataType: 'json', //make sure your service is actually returning json here
			success: function (data) {
                console.log("coco", data)
                for (let i = 0; i < data.length; i++) {
                    // console.log(data[i]);
                    if (data[i] === "PROSIT001") 
                      fetch_data(data[i])
                  }
            
				},
            error: function (errorMessage) { // error callback 
                console.log("error", errorMessage)
            }
			});
		};

    fetch_participants();
}
