$(function() {
	initPage();
});

$(window).bind('page:change', function(){
	initPage();
});

function initPage(){
    if($("#date_range_begin") && $("#date_range_end") && $("#date_range_button")){
	    a = {
		dateFormat: 'dd/mm/yy',
		dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'],
		dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
		dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
		monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
		monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
	    }
	    if($("#date_range_begin").prop('type')!="date"){
	    	$("#date_range_begin").datepicker(a);
	    	$("#date_range_end").datepicker(a);
	    }
	    $("#date_range_button").click(function(){
		search_by_date_range($("#date_range_begin").val(), $("#date_range_end").val());
	    });
    }
}

function search_by_date_range(date_range_begin, date_range_end){

	if(date_range_begin=='')return;
	else if(date_range_end=='')date_range_end=current_date();

	// coloca no formato correto
        separador = "/";
	if(date_range_begin.indexOf("-")!==-1) separador = "-";
	split = date_range_begin.split(separador);
	if(split[2].length==4)date_range_begin = split[2]+'-'+split[1]+'-'+split[0];
	split = date_range_end.split(separador);
	if(split[2].length==4)date_range_end = split[2]+'-'+split[1]+'-'+split[0];

	redirect_to = window.location.href;

	redirect_to = removeParam("date_range", redirect_to);
	redirect_to = removeParam("f[data][]", redirect_to, "date_range");

	redirect_to = insertParam("date_range","data:["+date_range_begin+"T00:00:00.000Z TO "+date_range_end+"T00:00:00.000Z]", redirect_to);
	redirect_to = insertParam("f[data][]","date_range",redirect_to);

	window.location.assign(redirect_to);
}

function current_date(){
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1;
	var yyyy = today.getFullYear();
	if(dd<10) {
	    dd='0'+dd
	} 
	if(mm<10) {
	    mm='0'+mm
	} 
	return dd+'/'+mm+'/'+yyyy;
}

function removeParam(key, sourceURL, val) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (var i = params_arr.length - 1; i >= 0; i -= 1) {
	    split_param = params_arr[i].split("=");
            param = split_param[0];
            value = split_param[1];
            if (typeof val !== 'undefined' && val==value && param === key) {
                params_arr.splice(i, 1);
            }
	    else if(typeof val === 'undefined' && param === key){
		params_arr.splice(i, 1);
	    }
        }
        rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

function insertParam(key,value,str)
{
    key = encodeURI(key); value = encodeURI(value);

    var s = str;
    var kvp = key+"="+value;

	if(s.indexOf("?")===-1){
		if(s.charAt(s.length-1)!='/')s = s+"/?";
		else s = s+"?";
	}

    var r = new RegExp("(&|\\?)"+key+"=[^\&]*");

    s = s.replace(r,"$1"+kvp);

    if(!RegExp.$1) {s += (s.length>0 ? '&' : '?') + kvp;};

    return s;
}
