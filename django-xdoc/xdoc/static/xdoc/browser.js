angular.module('browser', []).
    config(function($routeProvider) {
        $routeProvider.
            when('/', {controller: ListCtrl, templateUrl: '/static/xdoc/browser.html'}).
            when('/edit/:nodeId', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            otherwise({redirectTo: '/'});
    });


function ListCtrl($scope, $http) {

    $scope.load_data = function() {
        $http.get('/xdoc/api/node/').success(function(data) {
            $scope.count = data.count;
            $scope.next = data.next;
            $scope.previous = data.previous;
            $scope.nodes = data.results;
        });
    };

    $scope.load_data();
}


function EditCtrl($scope, $routeParams, $http) {
    $scope.nodeId = $routeParams.nodeId;

    $scope.load_data = function() {
        var url = '/xdoc/api/node/' + $scope.nodeId;
        $http.get(url).success(function(data) {
            $scope.node = data;
        });
    };

    $scope.load_data();
}