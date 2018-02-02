var app = {

    config: { 
	realtime_refresh_delay: 2.62,    // config options
	number_of_hours_to_run: 3
    },
    //
    runtime: {
	data: null,
	data_checksum: null,
	start_time: new Date(),
	networkFail: false
    },
    /*
    summary: null,
    questions: null,
    responses: null,
    responses_checksum: null,
    */
    
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
		"method": "POST",
		"error": function () {
		    app.runtime.networkFail = true;
		},
		"success": function (d) {

		    if (app.runtime.data_checksum)
			if (app.runtime.data_checksum === d.responses._items_checksum)
			    return;

		    app.runtime.data = d;
		    app.drawSummary();
		    app.drawTable();
		    app.runtime.data_checksum = d.responses._items_checksum;
		}});
    },

    loopDashData: function () {
	setInterval(function () {
		if (app.live_updates()) {
		    app.getDashData();
		} else {
		    app.drawLastUpdatedText(); // just the momentjs update
		}}, 1000 * app.config.realtime_refresh_delay);
    },
    
    drawSummary: function () {
	app.log("Drawing summary");
	app.displaySummaryDataPoints();
	app.drawLastUpdatedText();
    },

    drawTable: function () {
	var data = new google.visualization.DataTable();
	
	_.each(app.runtime.data.questions._items,
	       function (q) {
		   data.addColumn('string', q.question);
	       });

	data.addColumn('boolean', 'Completed');

	_.each(app.runtime.data.responses._items,
	       function (r) {

		   var responseData = [];
		   _.each(app.runtime.data.questions._items,
			  function (q) {
			      var answer = _.find(r.answers,
						  function (a) {
						      return a.question_id == q.id;
						  }),
				  tableCell = "";

			      if (answer) {

				  tableCell = answer.answer;

				  if (answer.in_progress == 'Y' && r.is_completed != 'Y') {
				      tableCell += '<span style="font-size:24px" ' +
					  'class="saving"><span>.</span><span>.</span><span>.</span></span>';
				  }
				  responseData.push(tableCell);

			      } else {
				  responseData.push(null);
			      }
			  });

		   if (r.is_completed == 'Y') {
		       responseData.push(true);
		   } else {
		       responseData.push(false);
		   }
		   
		   data.addRow(responseData);
	       });

	var table = new google.visualization.Table(document.getElementById('latable'));
	
	table.draw(data, {showRowNumber: false, allowHtml: true});
    },

    displaySummaryDataPoints: function () {
	app.log("Re-drawing summary");
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
