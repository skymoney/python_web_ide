/**
 * Created by cheng on 16/1/11.
 */

$(function(){
    var runtime_check = function(){
        $.ajax({
            url: '/api/runtime/check/',
            type: 'POST',
            success: function(data){
                if(data['status'] != 'ok'){
                    console.log("error occured: " + data['data']);
                }
            }
        })
    }

    //setInterval(runtime_check, 1000 * 60);
})