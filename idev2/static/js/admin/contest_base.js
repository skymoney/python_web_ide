/**
 * Created by cheng on 16/1/18.
 */

$(function(){
    $(".contest_delete").on("click", function(){
        var contest_id = $(this).parent().find("input").val();
        var dom = $(this);
        $.ajax({
            url: '/admin/contest/delete/',
            type: 'POST',
            data: {'contest_id': contest_id},
            dataType: 'json',
            success: function(data){
                if(data['status'] == 'ok'){
                    notify_type = 'success';
                }else{
                    notify_type = 'warning';
                }
                dom.notify(data['data'], notify_type, {position: 'top'});
            }
        })
    });

    $(".contest_publish").on("click", function(){
        var contest_id = $(this).parent().find("input").val();
        var dom = $(this);

        $.ajax({
            url: '/admin/contest/publish/',
            type: 'POST',
            data: {'contest_id': contest_id},
            dataType: 'json',
            success: function(data){
                if(data['status'] == 'ok'){
                    notify_type = 'success';
                }else{
                    notify_type = 'warning';
                }
                dom.notify(data['data'], notify_type, {position: 'top'});
            }
        })
    });
})