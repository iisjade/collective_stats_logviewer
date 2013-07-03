jQuery(document).ready(function() {
    $(document).on('ready', function(){
        $('dl.url-details dd').hide();
    });

    $(document).on('click', 'dt.url-help', function() {
        // Finds all the sibling dd elements of the link
        // clicked and toggles them as showing or not showing
        $(this).parents('dl').find('dd').toggle()

        // Grabs the url of the link that was clicked
        url = $(this).find('a').attr("data-url")

        // Assigns graph_div to the corresponding div that will be used
        // to render the graph for the link
        graph_div =  $(this).parents('dl').find('div.graph-placeholder').first()

        // create place to put fetch status so that we fetch data only once
        if (typeof $(graph_div).data("fetched") === "undefined") {
            // alert("in $.on(), fetched is undefined");
            $(graph_div).data("fetched", "no");
            // alert("in $.on(), fetched is now: " + $(graph_div).data("fetched"));
        }

        // start to plot
        plot(graph_div, url);
    });
});

function plot(graph_div, url) {

    // note: graph_div is a JQuery object

    // hold options for flot graph
    var options = {
		lines: {
			show: true,
		},
		points: {
			show: true,
            fillColor: "#0062E3",
		},
        xaxis: { mode: "time",
                 timeformat: "%M:%S",
                 minTickSize: [1, "second"]
        },
        yaxis: {
            ticks: [0,0.5,1,2,3,4,6,10],
        },
        legend: {
            show: true
        }
	};

    // hold data for flot to build the graph
    var data = [];

    // call back function when received data from server
    function onDataReceived(response) {
        // on success mark fetched = yes
        // alert("in onDataReceived(), fetched is: " + $(graph_div).data("fetched"));
        $(graph_div).data("fetched", "yes");
        // alert("in onDataReceived(), fetched is now: " + $(graph_div).data("fetched"));

        // iterate through data
        $.each(response.graph_data, function(key, value) {
            time = parseFloat(value.render_time);
            timestamp = (new Date(value.timestamp)).getTime();
            data.push([timestamp, time]);
        });

		$.plot(graph_div, [
        {
            label: "Render Time",
            data: data,
            color: "#0062E3",
        }
    ], options);

        // Find the <span>s for the link that was clicked and populated them with their
        // respective stats which were received during the ajax request.
        graph_div.parents('dl').find('.num-hits').text(response.stats_data.num_hits)
        graph_div.parents('dl').find('.cached-benefit').text(response.stats_data.cached_benefit)

        // For these next 2, jquery won't be able to find span.overall for a server choker,
        // or a span.avg for a slow page (since the avg is already set by Python as it's a header).
        // Doesn't seem to cause any problems, but is allowing it to fail like this good practice?
        // graph_div.parents('dl').find('.overall').text(response.stats_data.overall)
        var spanOverall = graph_div.parents('dl').find('.overall');
        // if the span = overall exists
        if (spanOverall.length > 0) {
            spanOverall.text(response.stats_data.overall)
        }

        // graph_div.parents('dl').find('.avg').text(response.stats_data.avg)
        var spanAvg = graph_div.parents('dl').find('.avg');
        // if the span = avg exists
        if (spanAvg.length > 0) {
            // alert("found .avg span")
            spanAvg.text(response.stats_data.avg)
        }
	};

    // check if data needed to be fetched
    if ((typeof $(graph_div).data("fetched") === "undefined") ||
        ($(graph_div).data("fetched") === "no")) {
            // alert("fetched is: " + $(graph_div).data("fetched"));
            // alert("about to fetch data");
            $.ajax({
                url: '/response_time_details/',
                type: "GET",
                data: {'url': url},
                dataType: "json",
                success: onDataReceived
        });
    } // end if
}
