/**
 * Created by cheng on 16/1/7.
 */
$(function(){
	var langTools = ace.require("ace/ext/language_tools");
	var editor = ace.edit("editor");

	editor.setTheme("ace/theme/monokai");
	editor.getSession().setMode("ace/mode/python");

	editor.setOptions({
		enableBasicAutocompletion: true,
		enableSnippets: true,
		enableLiveAutocompletion: true
	});

	$("#code_submit_btn").on("click", function(){
		var code = $("#editor").val();

		$.ajax({
			type: 'POST',
			url: '/code/submit/',
			data: {'code': code},
			dataType: 'json',
			success: function success(data){
				alert(data);
			},
		})
	})
})