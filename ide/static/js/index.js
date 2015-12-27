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
})