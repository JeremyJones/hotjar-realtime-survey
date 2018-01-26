var app = angular.module("dashboard", []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{ng ');
    $interpolateProvider.endSymbol(' ng}');
}]);


app.controller("dashboardCtrl", function($scope) {

    $scope.message = "Hello you guys";

    $scope.NameChange = function() {
        //console.log("NameChange: the value is " + $scope.name);
        $scope.fooname = "hello " + $scope.name;
    };
});