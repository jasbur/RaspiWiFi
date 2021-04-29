var shell = require('shelljs');
var fs = require('fs');


module.exports={
    change_hour,
    system_test,
    reset
}

function change_hour(req, res, next){
    let date = req.body.day;
    let hour = req.body.hour;
    console.log('date -s "'+date+' '+hour+'"');
    shell.exec('sudo date -s "'+date+' '+hour+'"');
    shell.exec('sudo hwclock -w');
    res.sendStatus(200);
    return;
}

function system_test(req, res, next){
    let test_duration = parseFloat(req.body.duration);
    let obj;
    fs.readFile('./device_config/device_config.json', 'utf8', function (err, data) {
        if (err){
            console.log(err);
            res.sendStatus(500);
            return;
        }
        if(data){
            obj = JSON.parse(data);
            obj.test.duration = test_duration;
            obj.test.status = true;
            save_config(obj);
            res.sendStatus(200);
            return;
        }else{
            res.sendStatus(400)
            return;
        }
    });
}

function reset(req, res, next){ 
    shell.exec('sudo reboot');
}

function save_config(new_config){
    JSON.stringify(new_config)
    fs.writeFileSync('./device_config/device_config.json', JSON.stringify(new_config));
    console.log("saved");
    return;
}