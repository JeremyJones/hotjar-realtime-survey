var app = {

    config: { 
	realtime_refresh_delay: 2.62,  // default refresh check time
	number_of_hours_to_run: 0.25,  // how long to run until going into standby
	enable_live_dots: false        // whether to try to display those dots on fields in progress
    },
    //
    runtime: {
	data: null,
	data_checksum: null,
	start_time: new Date(),
	last_data_time: null,
	networkFail: false
    },
    //
    live_updates: function () {  // -> bool
	if (app.runtime.networkFail) return false;
	
	var time_now = new Date();

	return(time_now.valueOf() - app.runtime.start_time.valueOf()
	       < (1000 * 3600 * app.config.number_of_hours_to_run));
    },
    // ---
    
    start: function () {
	app.getDashData();
	app.loopDashData();
    },

    getDashData: function () {
	$.ajax({"url": "/dashdata",
		"data": {"last": app.runtime.data_checksum},
		"processData": true,
		"method": "POST",
		"error": function () {
		    app.runtime.networkFail = true;
		},
		"success": function (d) {

		    if ("undefined" != d["status"])
			if (d.status == 304) return;

		    if (app.runtime.data_checksum)
			if (app.runtime.data_checksum === d.responses._items_checksum)
			    return;

		    app.runtime.data = d;
		    app.runtime.last_data_time = new Date();

		    app.drawDashboard();

		    app.runtime.data_checksum = d.responses._items_checksum; // after app.drawDashboard()
		}});
    },

    drawDashboard: function () {
	app.displaySummaryDataPoints();
	app.drawLastUpdatedText();
	app.drawTable();
    },
    
    loopDashData: function () {
	setInterval(
	    function () {
		if (app.live_updates()) {
		    app.getDashData();
		} else {
		    app.drawLastUpdatedText(); // just the momentjs update
		}}, 1000 * app.config.realtime_refresh_delay);
    },

    responses2datarows: function () { // generate the data table structure
	var dataRows = [];
	
	_.each(app.runtime.data.responses._items,
	       function (resp) {
		   var responseData = [];
		   
		   _.each(app.runtime.data.questions._items,
			  function (q) {
			      var answers = _.where(resp.answers,
						    function (ans) {
							return ans.question_id == q.id;
						    }),
				  answer = answers.join(', '),
				  tableCell = "",
				  showDots = false;

			      if (answer) {

				  if (q.answer_type === 'email' && answer.in_progress != 'Y')
				      tableCell = '&lt;<a class="text-muted" href="mailto:' +
				      answer.answer + '">' + answer.answer + '</a>&gt;';
				  else
				      tableCell = answer.answer;

				  showDots = (app.config.enable_live_dots &&
					      ((q.answer_type.substring(0,4) == 'text' || q.answer_type == 'email') &&
					       answer.in_progress == 'Y' && resp.is_completed != 'Y'));
				  
				  if (showDots) {
				      tableCell += '<span style="font-size:24px" ' +
					  'class="saving"><span>.</span><span>.</span>' +
					  '<span>.</span></span>';
				  }
				  responseData.push(tableCell);

			      } else {
				  responseData.push(null);
			      }
			  });

		   if (resp.is_completed == 'Y') {
		       responseData.push(true);
		   } else {
		       responseData.push(false);
		   }
		   
		   dataRows.push(responseData);
	       });

	return dataRows;
    },
    
    drawTable: function () {
	var data = new google.visualization.DataTable(),
	    table = new google.visualization.Table(document.getElementById('latable'));

	$("#numTableRows").text(app.runtime.data.responses._items.length);
	
	_.each(app.runtime.data.questions._items,
	       function (q) {
		   data.addColumn('string', q.question);
	       });

	data.addColumn('boolean', 'Completed');
	data.addRows(app.responses2datarows());
	table.draw(data, {page: 'enable', pageSize: 8,
			  width: '100%',
			  showRowNumber: false, allowHtml: true});
	$("table").addClass('table');

	// compensate for having to re-add this class on table page
	// changes
	setInterval(function () {
	    if (! $("table").hasClass('table')) {
		$("table").addClass('table');
	    }}, 250);
    },

    displaySummaryDataPoints: function () {
	//app.log("Re-drawing summary");
	app.fillDataConditional($("#sAnswerCount"), app.runtime.data.summary.num_responses);
	app.fillDataConditional($("#sAnswerAge"), app.runtime.data.summary.average_age);
	app.fillDataConditional($("#sAnswerGender"), app.runtime.data.summary.gender_ratio);
	app.fillDataConditional($("#sAnswerColors"), app.runtime.data.summary.colors);
    },

    fillDataConditional: function (target, content) {
	if (target.text() != content)
	    target.text(content);
    },

    drawLastUpdatedText: function () {
	$("#sLastUpdated").html(moment(app.runtime.data.summary.updated_at, "X").fromNow());
    },
    
    /*
      Application logging function defaults to no-op, optionally overridden.
     */
    log: function (m) {
	return;
    },
    log: function (m) {
	console.log(m);
    }
};
    
google.charts.load('current', {'packages':['table']});
google.charts.setOnLoadCallback(app.start);
