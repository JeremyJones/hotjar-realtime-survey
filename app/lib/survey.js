var newapp = angular.module("survey", []);

newapp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{ng ');
    $interpolateProvider.endSymbol(' ng}');
}]);


//


var app = {

    /*

    */

    "getQuestions": function() {
        $.ajax({
            'url': '/questions',
            'success': function() {
                app.log("Got questions");
            }
        });
    }
};