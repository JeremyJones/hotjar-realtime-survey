var app = {

    config: { 
	realtime_refresh_delay: 2.62,  // default refresh check time
	realtime_refresh_delay: 1,     // override refresh time
	number_of_hours_to_run: 0.25,  // how long to run until going into standby
	ft_live_dots: false   // live dots feature toggle: if true display animated dots inside live fields 
    },
    //
    runtime: {
	start_time: new Date(),
	data: null,
	data_checksum: null,
	last_data_time: null,
	networkFail: false
    },
    //
    start: function () {
	app.getDashData();  // first time fills quick as possible
	app.loopDashData();
    },
    //
    live_updates: function () {  // -> bool
	if (app.runtime.networkFail) return false;
	
	var time_now = new Date();

	return(time_now.valueOf() - app.runtime.start_time.valueOf()
	       < (1000 * 3600 * app.config.number_of_hours_to_run));
    },
    // ---
    setData: function (data, setChecksum=true) {
	app.runtime.data = data;
	app.runtime.last_data_time = new Date()

	if (setChecksum) app.setDataChecksum();
    },
    // --
    setDataChecksum: function () {
	app.runtime.data_checksum = d.responses._items_checksum;
    },
    // --
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
		    
		    app.setData(d, false);
		    app.drawDashboard();
		    app.setDataChecksum();
		}});
    },
    // --
    drawDashboard: function () {
	app.displaySummaryDataPoints();
	app.drawLastUpdatedText();
	app.drawTable();
    },
    // --
    loopDashData: function () {
	setInterval(
	    function () {
		if (app.live_updates()) {
		    app.getDashData();
		} else {
		    app.drawLastUpdatedText(); // just the momentjs update
		}}, 1000 * app.config.realtime_refresh_delay);
    },
    // --
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
				  answer = _.find(resp.answers,
						  function (ans) {
						      return ans.question_id == q.id;
						  }),
				  tableCell = "",
				  showDots = false;

			      //app.log("a are " + answers);
			      
			      if (answer) {

				  if (q.answer_type === 'email' && answer.in_progress != 'Y')
				      tableCell = '&lt;<a class="text-muted" href="mailto:' +
				      answer.answer + '">' + answer.answer + '</a>&gt;';
				  else
				      tableCell = answer.answer;

				  showDots = (app.config.ft_live_dots &&
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
    // --
    drawTable: function () {
	var data = new google.visualization.DataTable(),
	    table = new google.visualization.Table(document.getElementById('latable'));

	$("#numTableRows").text(app.runtime.data.responses._items.length);
	
	_.each(app.runtime.data.questions._items,
	       function (q) {
		   var columnHeader = q.question;
		   if (q.required == 'y') columnHeader += '<i class="fa fa-asterisk" title="Required"></i>*';
		   data.addColumn('string', columnHeader);
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
    // --
    formatMaleFemale: function (r) {
	var html = "", looper = null;

	for (looper in r) {
	    html += '<i class="fa fa-' + looper.toLowerCase() + '"></i> ' +
		looper + ' ' + r[looper] + '<br/>'
	}
	
	return html;
    },
    // --
    displaySummaryDataPoints: function () {
	//app.log("Re-drawing summary");
	var showData = app.fillDataConditional;  // only if they've changed
	
	showData($("#sAnswerCount"), app.runtime.data.summary.num_responses);
	showData($("#sAnswerAge"), (0.0 + app.runtime.data.summary.average_age).toFixed(1));
	showData($("#sAnswerGender"), app.formatMaleFemale(app.runtime.data.summary.gender_ratio));
	showData($("#sAnswerColors"), app.runtime.data.summary.top_3_colors.join(', '));
    },
    // --
    fillDataConditional: function (target, content) {
	if (target.html() != content)
	    target.html(content);
    },
    // --
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
