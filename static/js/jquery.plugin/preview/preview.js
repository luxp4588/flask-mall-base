(function($){
    $.fn.uploadImg = function(file, show, opt) {
        var me, c;
        opt = typeof(opt) == "object" ? opt : {};
        me = $(this);
        file = (typeof(file) == "string") ? $(file) : file;
        show = (typeof(show) == "string") ? $(show) : show;
        me.click(function(){
            file.trigger('click');
        });
        if(!window.applicationCache && typeof(opt.action) == "undefined") {
            alert("please use explore that support html5");
            return false;
        }else if(!window.applicationCache && typeof(opt.action) != "undefined") {
            var id = 'form' + parseInt(Math.random()*10000000);
            var submit_name = 'submit' + parseInt(Math.random()*10000000);
            var _html = '<iframe name="'+ submit_name +'" style="display:none;"></iframe>';
            $(_html).appendTo($('body'));
            file.change(function(){
                var fileInfo = $(this);
                fileInfo.wrap(function() {
                    return '<form id="'+ id +'" action="' + opt.action + '" method="POST" enctype="multipart/form-data" target="'+submit_name+'" />'
                });
                fileInfo.parent('form').submit(function(e) { e.stopPropagation(); }).submit()
            });

            return;
        }
        file.change(function(){
            var fileInfo = $(this),
                img,
                FR = new FileReader(),
                imgFile,ctx;
            imgFile  = fileInfo[0].files[0];
            FR.readAsDataURL(imgFile);
            FR.onload = function(){
                var result = this.result;
                img  = new Image();
                img.onload = function() {
                    ctx.drawImage(img, 0,0, 100, 100);
                }
                img.src = result;
            }
            if(!c) {
                c = document.createElement('canvas');
                c.setAttribute('width', (typeof(opt.width) == "undefined") ? 100 : opt.width);
                c.setAttribute('height', (typeof(opt.height) == "undefined") ? 100 : opt.height);
                $(c).appendTo(show);
                ctx = c.getContext('2d');
            }else {
                ctx = c.getContext('2d');
                ctx.clearRect(0, 0, (typeof(opt.width) == "undefined") ? 100 : opt.width, (typeof(opt.height) == "undefined") ? 100 : opt.height);
           }
        });
    };
})($);
(function(){
    $("#up_winxin_img").uploadImg('#weixin_img', '#show_up_img');
})();
