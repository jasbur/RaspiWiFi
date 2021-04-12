function system_reboot(){
    let reboot_check = confirm("Do you want to reboot the system?");
    if(reboot_check == true){
    $.ajax({
        method:"POST",
        url:"/system/reset"
    }).done(function(data){
        alert("The system is rebooting");
    });
    }
}