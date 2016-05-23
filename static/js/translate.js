/**
 * Created by xueweihan on 16/3/24.
 */

// 根据选择的关键字获取翻译
function get_translation(keyword){
    $.post("/translate", {keyword: keyword}, function(data){
        if(data.success) {
            var translation = data.data.translation;
            var explains = data.data.basic.explains;
            $("#translation-head").html(translation);
            $("#translation-body").html(explains.join('<br>'));
            $("#translation").css("display","block");
            change_color(keyword, data.data.count);
        }
        else{
            $("#translation-head").html(data.message);
            $("#translation-body").html('');
            $("#translation").css("display","block");
        }

    })

}

// 改变颜色
function change_color(keyword, count){

    var span_id = '.' + keyword.toLowerCase();
    if(count <=3){
        $(span_id).css("color","#40FF00");
    }
    else if (count <= 5){
        $(span_id).css("color", "#0000FF");
    }
    else if (count <= 10){
        $(span_id).css("color", "#8904B1");
    }
    else{
        $(span_id).css("color", "#FFBF00");
    }
}


$(document).ready(function(){
// 监听鼠标放开的操作，如果鼠标放时选择了内容则请求翻译；如果没有内容不请求翻译，同时不显示翻译框
    $(this).mouseup(function(e){
        $("#translation").css("left", e.pageX-30); // 获取鼠标的位置
        $("#translation").css("top", e.pageY+10);  // 用于结果的位置
        var txt = document.getSelection().toString().trim();  // 获取选择的内容

        if(txt){
            get_translation(txt);  // 获取翻译结果
        }
        else{
            $("#translation").css("display","none");  // 隐藏翻译框
        }
    })
})