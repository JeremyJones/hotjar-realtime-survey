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


var app = {

    summary: null,
    responses: null,

    drawSummary: function () {
	app.log("Drawing summary");
	$("#sAnswerCount").text(app.summary.num_responses);
    },
    
    start: function () {
	app.getSummary(function () {
		app.log("Summary returned");
		app.fillResponses(function () {
			app.log("Responses returned");
		    });
	    });
    },

    getSummary: function (cb=null) {
	$.ajax({url: "/summary",
		method: "POST",
		param_cb: cb,
		success: function (d) {
		    app.summary = d;
		    app.log("Assigned summary");
		    app.drawSummary();

		    if ("undefined" != typeof(this.param_cb))
			this.param_cb();
		}});
    },
    
    fillResponses: function (cb=null) {
	$.ajax({url: "/responses",
		method: "POST",
		param_cb: cb,
		success: function (d) {
		    app.responses = d._items;
		    app.log("Assigned responses");
		    app.log("my responses are " + app.responses.length + " long");

		    if ("undefined" != typeof(this.param_cb))
			this.param_cb();
		}});
    },
    
    log: function (m) {
	console.log(m);
    }
};
    
google.charts.load('current', {'packages':['table']});
google.charts.setOnLoadCallback(app.start);
