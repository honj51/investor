'use strict'

var express = require('express'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    redis = require('redis').createClient()

server.listen(8870)

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html')
})

app.use('/static', express.static(__dirname + '/static'))
app.use('/bootstrap', express.static(__dirname + '/bower_components/bootstrap/dist'))
app.use('/angularjs', express.static(__dirname + '/bower_components/angularjs'))


redis.psubscribe('platforms', 'application_data')

io.on('connection', function(socket) {
    
    redis.on('pmessage', function(pattern, channel, message) {
        if(pattern == 'platforms') {
            // console.log('---Got platforms data:' + message)
            socket.emit('platforms', message)
            console.log(channel)
            console.log(message)
            console.log('-----over ')
        }
        if(pattern == 'application_data') {
            console.log('---Got application_data data:' + message)
            // socket.emit('application_data', message)
        }
    })

})



redis.on('error', function(err) {
    console.log(err)
    console.log('可能数据没有链接')

})