// ONLOAD CHECK STATUS
$.post('indexExists.cgi', function(data) {
	// If built, display choice
	if (data) {
  		$('#statusResult').html("<p>Found a saved index.</p>");
  		$('#choice').show();
  	}
  	// if not built, build it
  	else {
  		$('#statusResult').html("<p>No saved index. Building it now...</p>");
  		
  		$.post('buildIndex.cgi', function(data){
  			$('#choice').html("<p>Done rebuilding the index</p>");
                	$('#search').fadeIn();
  		});  		
  	}
});

// USE OLD INDEX
$('#use').live("click", function(){
	$('#choice').hide();
	$('#search').fadeIn();
});

// MAKE NEW INDEX
$('#new').live("click", function(){
	$('#choice').html("<img src='loader.gif' />");
	$.post('buildIndex.cgi', function(data){
		$('#choice').html("<p>Done rebuilding the index</p>");
		$('#search').fadeIn();
        });
});

$('#searchForm').submit(function(e){
	e.preventDefault();
	var query = $('#searchQuery').val();
	var list = [];
	$('#results').show().html("<img src='loader.gif' />");
	$.getJSON('search.cgi', { "searchQuery": query },  function(data){
		for (prop in data) {
    			if (!data.hasOwnProperty(prop))
        			continue;
			var goodUrl = data[prop].substring(0, data[prop].length - 10)    			
			list.push("<li><a href='http://" + goodUrl + "'>http://" + goodUrl + "</a></li>");
		}
		
		$('#results').html("<ol>" + list.join(' ') + "</ol>");
	});
});

$('#showGraphs').click(function(){
	var dataPoints = [];
	$.getJSON('data.cgi', function(data){
	 	for (prop in data) {
        	if (!data.hasOwnProperty(prop))
            	continue;
         	dataPoints.push([parseInt(prop,10), data[prop]]);
         }
         console.log(dataPoints);
         
         var plot = $.plot($("#placeholder"),
                    	[ { data: dataPoints, label: "RSS/K"} ], {
                        		series: {
                            	lines: { show: true },
                            	points: { show: true }
                        		},
                        		grid: { hoverable: true, clickable: true }
       
                      	});
         
         
         
             	var previousPoint = null;
             	$("#placeholder").bind("plothover", function (event, pos, item) {
                 	$("#x").text(pos.x.toFixed(2));
                 	$("#y").text(pos.y.toFixed(2));
         
                     	if (item) {
                         	if (previousPoint != item.dataIndex) {
                            	 	previousPoint = item.dataIndex;
                             
                            		$("#tooltip").remove();
                            		var x = item.datapoint[0].toFixed(2),
                                 	    y = item.datapoint[1].toFixed(2);
                             
                             		showTooltip(item.pageX, item.pageY,
                                        	item.series.label + " at " + x + " = " + y);
                        		}
                     	}
                     	else {
                         	$("#tooltip").remove();
                         	previousPoint = null;            
                     	}
             	});
         
             	$("#placeholder").bind("plotclick", function (event, pos, item) {
                 	if (item) {
                     		plot.highlight(item.series, item.datapoint);
                 	}
             	});
         

	});

    	    	
    	function showTooltip(x, y, contents) {
    		$('<div id="tooltip">' + contents + '</div>').css( {
    	    	position: 'absolute',
    	    	display: 'none',
    	    	top: y + 5,
    	    	left: x + 5,
    	    	border: '1px solid #fdd',
    	    	padding: '2px',
    	    	'background-color': '#fee',
    	    	opacity: 0.80
    		}).appendTo("body").fadeIn(200);
    	}
});
