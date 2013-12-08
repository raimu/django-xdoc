var browser = angular.module('BrowserApp', ['ngRoute']).
    config(function($routeProvider) {
       $routeProvider.
            when('/', {controller: ListCtrl, templateUrl: '/static/xdoc/browser.html'}).
            when('/add/:addNodeName', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            when('/edit/:nodeId', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            when('/detail/:nodeId', {controller: DetailCtrl, templateUrl: '/static/xdoc/detail.html'}).
            otherwise({redirectTo: '/'});
    });


browser.factory('BrowserService', function($http) {
   return {
        getConfig: function() {
            return $http.get('/xdoc/api/config')
                .then(function(result) {
                    return result.data;
                });
        }
   }
});


browser.run(function ($rootScope) {
    $rootScope.start = null;
    $rootScope.q = null;
    $rootScope.parent_node = null;
});


function ListCtrl($scope, $http, $rootScope, BrowserService) {
    "use strict";

    $scope.loading = false;
    $scope.config = BrowserService.getConfig();

    $scope.loadNode = function() {
        $scope.loading = false;
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
            $scope.loading = true;
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
            var iframe = $('iframe');
            $scope._adjustIframeHeight(iframe);
            iframe.contents().click(function(){
                $scope._adjustIframeHeight(iframe);
            });
            iframe.contents().keypress(function(){
                $scope._adjustIframeHeight(iframe);
            });
            iframe.contents().mousemove(function(){
                $scope._adjustIframeHeight(iframe);
            });
            iframe.contents().scroll(function(){
                $scope._adjustIframeHeight(iframe);
            });
        }).appendTo('#iframeContent');
    };

    $scope._adjustIframeHeight = function(iframe) {
        iframe.height(iframe.contents().find('html').height() + 30);
    };

    $scope._generate_url = function() {
        if('addNodeName' in $routeParams) {
            return '/xdoc/add/' + $routeParams['addNodeName'];
        }
        return '/xdoc/edit/' + $routeParams['nodeId'];
    };

    $scope.init = function() {
        $scope.insert_iframe();
    };
    $scope.init();
}