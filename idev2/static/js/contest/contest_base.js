/**
 * Created by cheng on 16/1/13.
 */

$(".join_btn").on("click", function(){
    var contest_id = $("#contest_id").parent().find("input").val();
    var dom = $(this);

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
            dom.notify(data['data'], notify_type, {position: 'right'});

            //btn更改为已参加
            var origin_class = dom.attr("class");
            dom.attr("class", origin_class.replace("btn-success", "btn-default"));
            dom.html("已报名");
            dom.removeAttr("id");
        }
    })
})