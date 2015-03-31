'use strict'

var express = require('express'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    redis = require('redis').createClient(),
    exec = require('child_process').exec



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
            socket.emit('platforms', message)
        }
        if(pattern == 'application_data') {
            socket.emit('application_data', message)
        }
    })

    socket.on('task', function(data) {
        if (data == 'start') {
            exec("cd " +  __dirname  + " && cd .. && source bin/activate && cd octopus && python machine.py", function(err, stdout, stderr) {
                console.log(stdout)
            })
        }
        
    })
})



redis.on('error', function(err) {
    console.log(err)
    console.log('可能数据没有链接')

})