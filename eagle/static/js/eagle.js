'use strict'
// var socket = io('http://localhost:8870')

var platform = {
    'wsloan': '温商贷',
    'wzdai': '温州贷',
    'zfxindai': '紫枫信贷',
    'zhaoshangdai': '招商贷',
    'itouzi': '爱投资',
    'nonobank': '诺诺磅客',
    'sidatz': '四达投资',
    'zhongbaodai': '中宝财富',
    'zibenzaixian': '资本在线',
    'yiqihao': '一起好',
    'yududai': '渝都贷'
}

angular.module('eagle',[])
.factory('socket', function ($rootScope) {
    var socket = io('http://localhost:8870')
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
        template: '<a href="#" >{{data.platform[key]}}<span class="badge pull-right">{{value - 1}}</span></a>'
    }
})
.controller('platforms', function($scope, socket) {
    $scope.data = {
        item : {},
        platform : platform,
        application_data: [],
        is_refresh: false
    }

    $scope.refresh = function() {
        $scope.data.application_data = []
        $scope.data.is_refresh = true
        socket.emit('task', 'start')
    }

    socket.on('platforms', function(data) {
        $scope.data.item = JSON.parse(data)
        $scope.data.is_refresh = false
    })

    socket.on('application_data', function(data) {
        $scope.data.application_data.push(JSON.parse(data))
        $scope.data.is_refresh = false
    })

})
