var express = require('express');
var app = express();
let path    = require("path");
let bodyParser = require('body-parser');
let configure_device = require('./router/configure_device');
let index = require('./router/index');
let time = require('./router/real_time');
let configure_system = require('./router/system');
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true,
    limit: '50mb',
    parameterLimit: 1000000}));

    app.use(bodyParser.json({limit: '50mb'}));
    app.use(express.static(path.join(__dirname, 'public')));

app.use("/device", configure_device);

app.use("/system", configure_system);

app.use("/time", time);

app.use("/", index);

app.listen(3000, function () {
  console.log('Listening on port 3000!');
});