/**
 * Created by XueWeiHan on 16/7/1 下午5:38.
 * 用户首页js
 */

function readURL(input) {
    $('#uploadButton').attr('disabled', 'disabled');
    var file = input.files[0];
    if (file.type !== 'image/jpeg' && file.type !== 'image/png' && file.type !== 'image/gif') {
        $('#blah').attr('src', 'http://7xv88n.com1.z0.glb.clouddn.com/default_avatar.jpg');
        alert('不是有效的图片文件!');
        return;
    } else if (file.size > 2*1024*1024) {
        $('#blah').attr('src', 'http://7xv88n.com1.z0.glb.clouddn.com/default_avatar.jpg');
        alert('图片不能超过2M');
        return;
    } else {
        // 展示上传的图片
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#blah').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
        $('#uploadButton').removeAttr('disabled');
    }
}

$("#imgInp").change(function(){
    readURL(this);
});

$("#form1").on('submit', function (e) {
    e.preventDefault();
    var user_uid = $('#uid').val();
    // 点击上传后按钮展示为‘上传中’
    $(uploadButton).button('上传中...');
    $.ajax({
       type:'POST',
       url: '/user/'+user_uid,
       dataType: 'json',
       data: new FormData($('#form1')[0]),
       contentType: false,
       cache: false,
       processData:false,
       success:function(data) {
           alert('上传成功！');
           window.location.reload();

       },
       error:function(data){
           alert('上传图片出错！');
           window.location.reload();

       }
    });
});
