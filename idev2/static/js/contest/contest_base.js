/**
 * Created by cheng on 16/1/13.
 */

$("#join_btn").on("click", function(){
    var contest_id = $("#contest_id").val();

    $.ajax({
        url: '/contest/join/',
        type: 'POST',
        data: {'contest_id': contest_id},
        dataType: 'json',
        success: function(data){
            var notify_type = '';
            if(data['status'] == 'ok'){
                notify_type = 'success'
            }else{
                notify_type = 'warning'
            }
            $("#join_btn").notify(data['data'], notify_type, {position: 'right'});

            //btn更改为已参加
            var origin_class = $("#join_btn").attr("class");
            $("#join_btn").attr("class", origin_class.replace("btn-success", "btn-default"));
            $("#join_btn").html("已报名");
            $("#join_btn").removeAttr("id");
        }
    })
})