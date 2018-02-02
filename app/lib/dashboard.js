/*
var newapp = angular.module("dashboard", []);

newapp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{ng ');
    $interpolateProvider.endSymbol(' ng}');
}]);


newapp.controller("dashboardCtrl", function($scope) {

    $scope.message = "Hello";

    $scope.NameChange = function() {
        //console.log("NameChange: the value is " + $scope.name);
        $scope.fooname = "hello " + $scope.name;
    };
});


*/
var app = {

    realtime_refresh_delay: 2.62,    // config option
    //
    summary: null,
    responses: null,
    responses_checksum: null,
    //
    start_time: new Date(),
    networkFail: false,
    live_updates: function () {  // -> bool
	var time_now = new Date();

	if (app.networkFail) return false;
	
	return time_now.valueOf() - app.start_time.valueOf() < (43200 * 1000);
    },
    // ---
    
    start: function () {
	app.getDashData();
	app.loopDashData();
	
	// setTimeout(function () {
	// 	app.loopDashData();
	//     }, 1000 * app.realtime_refresh_delay);
	/*
	app.getSummary(function () {
		app.log("Summary returned");
		app.getResponses();
		
		setInterval(function () {
			if (app.live_updates()) {
			    app.getResponses();
			    app.getSummary();
			}}, 1000 * app.realtime_refresh_delay);
	    });
	*/
    },

    getDashData: function () {
	$.ajax({"url": "/dashdata",
		"method": "POST",
		"success": function (d) {
		    app.summary = d.summary;
		    app.responses = d.responses._items;
		    app.responses_checksum = d.responses._items_checksum;

		    app.drawSummary();
		    return;
		}});
    },

    loopDashData: function () {
	setInterval(function () {
		if (app.live_updates()) {
		    app.getDashData();
		    /*
		    app.getResponses();
		    app.getSummary();
		    */
		}}, 1000 * app.realtime_refresh_delay);
    },
    
    /*
    getSummary: function (cb=null) {
	$.ajax({url: "/summary",
		method: "POST",
		param_cb: cb,
		error: function () {
		    app.networkFail = true;
		},
		success: function (d) {
		    app.networkFail = false;
		    app.summary = d;
		    app.log("Assigned summary");
		    app.drawSummary();

		    if ("function" == typeof(this.param_cb))
			this.param_cb();
		}});
    },
    */
    
    drawSummary: function () {
	app.log("Drawing summary");
	app.displaySummaryDataPoints();
	app.drawLastUpdatedText();
    },
    
    displaySummaryDataPoints: function () {
	app.log("Re-drawing summary");
	app.fillDataConditional($("#sAnswerCount"), app.summary.num_responses);
	app.fillDataConditional($("#sAnswerAge"), app.summary.average_age);
	app.fillDataConditional($("#sAnswerGender"), app.summary.gender_ratio);
	app.fillDataConditional($("#sAnswerColors"), app.summary.colors);
    },

    fillDataConditional: function (target, content) {
	if (target.text() != content)
	    target.text(content);
    },

    drawLastUpdatedText: function () {
	$("#sLastUpdated").html(moment(app.summary.updated_at, "X").fromNow());
    },
    
    /*
    getResponses: function (cb=null) {
	$.ajax({url: "/responses",
		method: "POST",
		param_cb: cb,
		error: function () {
		    app.networkFail = true;
		},
		success: function (d) {
		    app.networkFail = false;
		    app.responses = d._items;
		    app.responses_checksum = d._items_checksum;
		    
		    app.log("Assigned responses");
		    app.log("my responses are " + app.responses.length + " long");

		    if ("function" == typeof(this.param_cb))
			this.param_cb();
		}});
    },
    */
    
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
