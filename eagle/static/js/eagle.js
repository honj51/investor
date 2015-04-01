'use strict'

angular.module('eagle',[])
.factory('socket', function ($rootScope) {
    var socket = io(document.URL)
    return {
        on: function (eventName, callback) {
            socket.on(eventName, function () {  
                var args = arguments
                $rootScope.$apply(function () {
                    callback.apply(this, args)
                });
            });
        },
        emit: function(eventName, data, callback) {
            socket.emit(eventName, data, function() {
                var args = arguments
                $rootScope.$apply(function() {
                    callback.apply(this, args)
                })
            })
        }
    };
})
.directive('navContent', function() {
    return {
        restrict: 'A',
        scope: true,
        replace: true,
        template: '<a href="#" >{{key}}<span class="badge pull-right">{{value - 1}}</span></a>'
    }
})
.controller('platforms', function($scope, socket) {
    $scope.data = {
        item : {},
        application_data: [],
        is_refresh: false
    }

    $scope.refresh = function() {
        $scope.data.application_data = []
        $scope.data.is_refresh = true
        socket.emit('task', 'start')
    }

    socket.on('platforms', function(data) {
        $scope.data.item = data
        $scope.data.is_refresh = false
    })

    socket.on('application_data', function(data) {
        $scope.data.application_data.push(data)
        $scope.data.is_refresh = false
    })

})
