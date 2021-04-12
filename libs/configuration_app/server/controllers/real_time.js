'use strict'

module.exports = {
    get_time
}

function get_time(req, res, next){
    let date_hour = String(new Date().getHours());
    let date_minutes = String(new Date().getUTCMinutes());
    let date_seconds = String(new Date().getUTCSeconds());
    let date_day = String(new Date().getDate());
    let date_week_day = String(parseInt(new Date().getDay())-1);
    let date_month = String(parseInt(new Date().getMonth())+1);
    let date_year = String(new Date().getFullYear());
    
    var weekday=new Array(7);
        weekday[0]="Monday";
        weekday[1]="Tuesday";
        weekday[2]="Wednesday";
        weekday[3]="Thursday";
        weekday[4]="Friday";
        weekday[5]="Saturday";
        weekday[6]="Sunday";

    res.send({
        hour:date_hour,
        minutes:date_minutes,
        seconds:date_seconds,
        day:date_day,
        week_day:weekday[date_week_day],
        month:date_month,
        year:date_year
    });
}