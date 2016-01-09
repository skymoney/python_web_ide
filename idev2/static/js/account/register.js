/**
 * Created by cheng on 16/1/9.
 */

$(function(){
    $("#register_btn").on("click", function(){
        var email = $("#email").val();
        var name = $("#username").val();
        var passwd = $("#passwd").val();

        $.ajax({
            url: '/register/',
            type: 'POST',
            data: {'name': name, 'email': email, 'passwd': passwd},
            dataType: 'json',
            success: function(data){
                $("#error_label").text(data['data']);
            }
        })
    });
})