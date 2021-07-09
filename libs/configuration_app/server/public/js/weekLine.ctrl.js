$("#weekCal").weekLine({
    mousedownSel: false,
    onChange: function () {
        let get_cycles = [];
            $("#selectedDays").html(
                    $(this).weekLine('getSelected')
            );

            for(let i =0;i<$('.selectedDay').length;i++){
                get_cycles.push(document.getElementsByClassName("selectedDay").item(i).innerHTML);
            }
            console.log(get_cycles);
            $.ajax({
                method:"GET",
                url:"/device/config",
                data:{
                    days:get_cycles
                }
            }).done(function(data){
                console.log(data);
                document.getElementById("table_body").innerHTML="";
                document.getElementById("table_body").innerHTML=data;
            }).fail(function(err){
                document.getElementById("table_body").innerHTML="";
                document.getElementById("table_body").innerHTML="<tr class='tr-shadow'><td></td><td></td><td class='text-right'><span>No cycles configured</span></td></tr>"
            })
    }
});