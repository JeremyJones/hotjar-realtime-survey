var newapp = angular.module("dashboard", []);

newapp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{ng ');
    $interpolateProvider.endSymbol(' ng}');
}]);


newapp.controller("dashboardCtrl", function($scope) {

    $scope.message = "Hello you guys";

    $scope.NameChange = function() {
        //console.log("NameChange: the value is " + $scope.name);
        $scope.fooname = "hello " + $scope.name;
    };
});



var app = {

    responses: null,

    start: function () {
	app.fillResponses(function () {
		app.log("Ready");
	    });
    },
    
    fillResponses: function (cb=null) {
	$.ajax({url: "/responses",
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
}
    
google.charts.load('current', {'packages':['table']});
//google.charts.setOnLoadCallback(drawTable);
google.charts.setOnLoadCallback(app.start);
	    
//Backbone.Collection.extend({url:'/responses'});
//responses.fetch();


