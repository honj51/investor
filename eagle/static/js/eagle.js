'use strict'
// var socket = io('http://localhost:8870')

var platform = {
    'wsloan': '温商贷',
    'wzdai': '温州贷',
    'zfxindai': '紫枫信贷',
    'zhaoshangdai': '招商贷',
    'itouzi': '爱投资',
    'nobank': '诺诺磅客',
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
                var args = arguments;
                $rootScope.$apply(function () {
                    callback.apply(this, args)
                });
            });
        }
    };
})
.controller('platforms', function($scope, socket) {
    $scope.item = {}

    socket.on('platforms', function(data) {
        console.log(data)
        $scope.item = JSON.parse(data)
    })

})
