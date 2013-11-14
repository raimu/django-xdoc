var app = angular.module('browser', []).
    config(function($routeProvider) {
        $routeProvider.
            when('/', {controller: ListCtrl, templateUrl: '/static/xdoc/browser.html'}).
            when('/add/:addNodeName', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            when('/edit/:nodeId', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            when('/detail/:nodeId', {controller: DetailCtrl, templateUrl: '/static/xdoc/detail.html'}).
            otherwise({redirectTo: '/'});
    });

app.run(function ($rootScope) {
    $rootScope.start = null;
    $rootScope.q = null;
    $rootScope.parent_node = null;
});


function ListCtrl($scope, $http, $rootScope) {
    "use strict";

    $scope.loadConfig = function() {
        $http.get('/xdoc/api/config').success(function(data){
            $scope.config = data;
        });

    };

    $scope.loadNode = function() {
        var config = {params: {
            parent_node: $rootScope.parent_node,
            start: $rootScope.start,
            q: $rootScope.q
        }};
        $http.get('/xdoc/api/node/', config).success(function(data) {
            $rootScope.parent_node = data.parent_node;
            $rootScope.start = data.start;
            $rootScope.q = data.q;
            $scope.count = data.count;
            $scope.paginate = data.paginate;
            $scope.path = data.path;
            $scope.nodes = data.results;
        });
    };

    $scope.runSearch = function() {
        $rootScope.start = 0;
        $rootScope.q = $scope.q;
        $scope.loadNode();

    };

    $scope.nextPage = function() {
        $rootScope.start += $scope.paginate;
        $scope.loadNode();
    };

    $scope.previousPage = function() {
        $rootScope.start -= $scope.paginate;
        $scope.loadNode();

    };

    $scope.changeDirectory = function(nodeId) {
        $rootScope.parent_node = nodeId;
        $scope.loadNode();
    };

    $scope.pageEnd = function() {
        return Math.min($scope.start + $scope.paginate, $scope.count)
    };

    $scope.selectPath = function(nodeId) {
        $rootScope.parent_node = nodeId;
        $scope.loadNode();
    };

    $scope.open = function(nodeIndex) {
        var node = $scope.nodes[nodeIndex];
        if (node.has_children) {
            $rootScope.parent_node = node.id;
            $scope.loadNode();
        }
        else {
            location.href = "#/edit/" + node.id;
        }
    };

    $scope.init = function() {
        $scope.loadConfig();
        $scope.loadNode();
    };

    $scope.init();
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
            iframe.height(iframe.contents().find('html').height() + 30);
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