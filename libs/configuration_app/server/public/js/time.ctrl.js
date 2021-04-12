$( document ).ready(function() {
    timer_function();
});

function get_time(){
    $.ajax({
        method:"GET",
        url:"/time"
    }).done(function(data){
        let meridian = "AM";
        if(parseInt(data.hour)==12){
            meridian = "PM"
        }

        if(parseInt(data.hour) == 0){
            data.hour = 12;
            meridian = "AM"
        }

        if(parseInt(data.hour)>12){
            data.hour = parseInt(data.hour) - 12;
            meridian = "PM"
        }

        if(data.hour.length==1){
            data.hour="0"+String(data.hour);
        }

        if(data.minutes.length==1){
            data.minutes="0"+String(data.minutes);
        }

        if(data.seconds.length==1){
            data.seconds="0"+String(data.seconds);
        }

        document.getElementById("real_time").innerHTML="";
        document.getElementById("real_time").innerHTML=data.week_day+" "+data.day+"/"+data.month+"/"+data.year+" "+data.hour+":"+data.minutes+":"+data.seconds+" "+meridian;
        tt = timer_function();
    })
}

function timer_function(){
    var refresh=1000; // Refresh rate in milli seconds
    mytime = setTimeout('get_time();',refresh)
}