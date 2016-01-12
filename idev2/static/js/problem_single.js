/**
 * Created by cheng on 16/1/7.
 */
$(function () {
    var langTools = ace.require("ace/ext/language_tools");
    var editor = ace.edit("editor");

    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");

    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true
    });

    $("#code_submit_btn").on("click", function () {
        var code = editor.getValue();

        $.ajax({
            type: 'POST',
            url: '/code/submit/',
            data: {'code': code},
            dataType: 'json',
            success: function success(data) {
                var sub_res_obj = eval(data);

                var query_id = setInterval(function (submission_id) {
                    // 调用接口轮询提交状态，每秒钟轮询
                    // 如果状态成功或失败，停止轮询
                    // 状态分为 running accepted failed
                    $.ajax({
                        url: '/api/submission/query/',
                        type: 'POST',
                        data: {'submission_id': submission_id},
                        dataType: 'json',
                        success: function (data) {
                            if(data['status'] == 'ok' && data['data'] != 'running'){
                                // 轮询完成,停止轮询
                                clearInterval(query_id);
                                $("#code_score").html(data['score'])
                                $("#code_info").html(data['info'])
                            }else{
                                $("#code_info").html(data['data'])
                            }
                        }
                    })
                }, 1000, sub_res_obj['submission']);
            },
        })
    })
})