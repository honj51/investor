'use strict'

var express = require('express'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    nconf = require('nconf'),
    redis = require('redis').createClient(),
    exec = require('child_process').exec


nconf.file(__dirname + '/../config.json')
nconf.set('port', nconf.get('port') || 8870)


server.listen(nconf.get('port'))



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

            socket.emit('platforms', function() {
                message = JSON.parse(message)
                for (var i in message) {
                    message[nconf.get('platform')[i]] = message[i]
                    delete message[i]
                }
                return message
            }())
        }
        if(pattern == 'application_data') {
            socket.emit('application_data', function() {
                message = JSON.parse(message)
                message['platform'] = nconf.get('platform')[message['platform']]
                return message
            }())
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
})