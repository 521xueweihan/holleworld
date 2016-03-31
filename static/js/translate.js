/**
 * Created by xueweihan on 16/3/24.
 */

// 根据选择的关键字获取翻译
function get_translation(keyword){
    $.get("/translate", {keyword: keyword}, function(data){
        var data_list = [];
        var translation = data.data.translation;
        data_list.push(translation);
        var explains = data.data.basic.explains;
        for (var i = 0;i < explains.length; i++){
            data_list.push(explains[i]);
        }

        $("#translation").html(data_list.join(''));
        $("#translation").css("display","block");
    })
}

$(document).ready(function(){
// 监听鼠标放开的操作，如果鼠标放时选择了内容则请求翻译；如果没有内容不请求翻译，同时不显示翻译框
    $(this).mouseup(function(e){
        $("#translation").css("left", e.pageX-30); // 获取鼠标的位置
        $("#translation").css("top", e.pageY+10);  // 用于结果的位置
        var txt = document.getSelection().toString();  // 获取选择的内容

        if(txt){
            get_translation(txt);  // 获取翻译结果
        }
        else{
            $("#translation").css("display","none");  // 隐藏翻译框
        }
    })
})