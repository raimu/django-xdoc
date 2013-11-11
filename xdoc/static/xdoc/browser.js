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

    $scope.insert_iframe = function() {
        var element = $('<iframe src="/xdoc/edit/' + $scope.nodeId+'"' +
            'style="width: 100%; border: none;" />');
        $(element).load(function(){
            var iframe = $('iframe')
            iframe.height(iframe.contents().find('html').height());
        }).appendTo('#iframeContent');
    };

    $scope.on_save = function() {
        $('iframe').contents().find('form').submit()
    };

    $scope.init = function() {
        $scope.insert_iframe();
    };
    $scope.init();
}