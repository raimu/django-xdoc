angular.module('browser', []).
    config(function($routeProvider) {
        $routeProvider.
            when('/', {controller: ListCtrl, templateUrl: '/static/xdoc/browser.html'}).
            when('/add/:addNodeName', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            when('/edit/:nodeId', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            when('/detail/:nodeId', {controller: DetailCtrl, templateUrl: '/static/xdoc/detail.html'}).
            otherwise({redirectTo: '/'});
    });


function ListCtrl($scope, $http) {

    $scope.load_data = function() {
        $http.get('/xdoc/config').success(function(data){
            $scope.config = data;
        });
        $http.get('/xdoc/api/node/').success(function(data) {
            $scope.count = data.count;
            $scope.next = data.next;
            $scope.previous = data.previous;
            $scope.nodes = data.results;
        });
    };

    $scope.load_data();
}


function DetailCtrl($scope, $routeParams, $http) {

    $scope.load_data = function() {
        var url = '/xdoc/api/node/' + $routeParams['nodeId']
        $http.get(url).success(function(data) {
            $scope.node = data;
        });
    };

    $scope.load_data();
}


function EditCtrl($scope, $routeParams) {

    $scope.insert_iframe = function() {
        var element = $('<iframe src="' + $scope._generate_url() +'"' +
            'style="width: 100%; border: none;" />');
        $(element).load(function(){
            var iframe = $('iframe')
            iframe.height(iframe.contents().find('html').height());
        }).appendTo('#iframeContent');
    };

    $scope._generate_url = function() {
        if('addNodeName' in $routeParams) {
            return '/xdoc/add/' + $routeParams['addNodeName'];
        }
        return '/xdoc/edit/' + $routeParams['nodeId'];
    }

    $scope.on_save = function() {
        $('iframe').contents().find('form').submit()
    };

    $scope.init = function() {
        $scope.insert_iframe();
    };
    $scope.init();
}