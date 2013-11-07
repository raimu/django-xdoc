angular.module('browser', []).
    config(function($routeProvider) {
        $routeProvider.
            when('/', {controller: ListCtrl, templateUrl: '/static/xdoc/browser.html'}).
            when('/edit/:nodeId', {controller: EditCtrl, templateUrl: '/static/xdoc/edit.html'}).
            otherwise({redirectTo: '/'});
    });

function ListCtrl($scope) {
    $scope.folder = "/static/xdoc/lib/icons/places/folder.png";
    $scope.text = "/static/xdoc/lib/icons/mimetypes/text-x-nfo.png";
    $scope.xml = "/static/xdoc/lib/icons/mimetypes/text-xml.png";
    $scope.nodes = [
        {
            id: 1,
            name: "Foo",
            thumbnail: $scope.folder
        },
        {
            id: 2,
            name: "HelloWorld.txt",
            thumbnail: $scope.text
        },
        {
            id: 3,
            name: "Bar.txt",
            thumbnail: $scope.text
        },
        {
            id: 4,
            name: "Baz.txt",
            thumbnail: $scope.xml,
            tags: ["foo", "bar", "baz"]
        },
        {
            id: 5,
            name: "HelloWorld.txt",
            thumbnail: $scope.text
        },
        {
            id: 6,
            name: "Bar.txt",
            thumbnail: $scope.text
        },
        {
            id: 7,
            name: "Baz.txt",
            thumbnail: $scope.xml,
            tags: ["Hello", "World"]
        },
        {
            id: 8,
            name: "HelloWorld.txt",
            thumbnail: $scope.text
        },
        {
            id: 9,
            name: "Bar.txt",
            thumbnail: $scope.text
        }
    ];
}


function EditCtrl($scope, $routeParams) {
    $scope.nodeId = $routeParams.nodeId;
    $scope.node = {
        id: $scope.nodeId,
        name: "Hello World"
    };
}