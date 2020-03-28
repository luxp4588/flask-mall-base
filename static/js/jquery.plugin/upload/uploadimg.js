(function($){
	$.fn.uploadFileFrame = function(uploadFile, _opt) {
		var opt = {
          action: '',
          autoSubmit: true,
          manualSubmit: null,
          params: [],
          onStart: function() {},
          onSuccess: function() {}
        },
        selectModel = $(this),
        upFile = $(uploadFile),
        iframe_id;
        if(_opt) {
        	$.extend(opt, _opt);
        }
		if(!opt.action) {
			alert("请设置要上传的地址！！");
			return false;
		}
		if(!opt.autoSubmit && !$(opt.manualSubmit).length) {
			alert("请确保手动上传的按钮设置正确");
			return false;
		}

		selectModel.click(function(){
			upFile.trigger('click');
		});
		
        iframe_id = 'jquery-iframe-' + parseInt(Math.random() * 10000000);        
        upFile.wrap(function() {
        	return '<form action="' + opt.action + '" method="POST" enctype="multipart/form-data" target="'+iframe_id+'" />';
        });
        $('body').after('<iframe width="0" height="0" style="display:none;" name="'+iframe_id+'" id="'+iframe_id+'" />');
		
		$('#'+iframe_id).get(0).onload = function() {
			var me = $(this);
			opt.onSuccess.call(upFile, JSON.parse(me.contents().text()));
        };

		if(opt.autoSubmit) {
			upFile.change(function(){
				_uploadFunc.call(this);
			});
		}else {
			$(opt.manualSubmit).click(function(){
				_uploadFunc.call(upFile);
			});
		}
		var _uploadFunc = function() {
			//this 对象指向upFile
			var me = $(this);
			if(typeof(me[0].files) == "undefined" || typeof(me[0].files[0]) == "undefined") {
				alert("请确保uploadFile是input[type=file]文件，并且选择了文件");
				return false;
			}
			opt.onStart.apply(me, opt.params);
			$("form[target=" + iframe_id + "]").submit();
		};
	};
	$.fn.uploadFile = function(uploadFile, _opt) {
		var opt = {
          action: '',
          autoSubmit: true,
          manualSubmit: null,
          params: [],
          onStart: function() {},
          onSuccess: function() {},
          onError: function() {},
          onAbort: function() {},
          onFail: function() {}
        },
        upFile = $(uploadFile),

        //系统弹出的文件选择模态框
        selectModel = $(this);
        if(_opt) {
        	$.extend(opt, _opt);
        }
		if(typeof(window.FormData) != "function") {
			alert("您的浏览器不支持HTML5无刷新上传，请使用现代浏览器！");
			return false;
		}
		if(!opt.action) {
			alert("请设置要上传的地址！！");
			return false;
		}
		if(!opt.autoSubmit && !$(opt.manualSubmit).length) {
			alert("请确保手动上传的按钮设置正确");
			return false;
		}

		selectModel.click(function(){
			upFile.trigger('click');
		});
		if(opt.autoSubmit) {
			upFile.change(function(){
				_uploadFunc.call(this);
			});
		}else {
			$(opt.manualSubmit).click(function(){
				_uploadFunc.call(upFile);
			});
		}

		var _uploadFunc = function(){
			var me = $(this),
        	formData;
			if(typeof(me[0].files) == "undefined" || typeof(me[0].files[0]) == "undefined") {
				alert("请确保uploadFile是input[type=file]文件，并且选择了文件");
				return false;
			}
			formData = new FormData();
			formData.append('up_file', me[0].files[0]);

			var xhr = new XMLHttpRequest();
			xhr.open('POST', opt.action);

			xhr.onloadstart = function() {
				opt.onStart.apply(me, opt.params);
			}

		    xhr.onerror = function() {
		        opt.onError.apply(me, opt.params);
		        return false;
		    };

		    xhr.onabort = function() {
		    	opt.onAbort.apply(me, opt.params);
		    	return false;
		    };

		    xhr.onreadystatechange = function() {
		        if (xhr.readyState == 4 && xhr.status == 200) {
		            opt.onSuccess.call(me, JSON.parse(xhr.responseText));
		        } else if (xhr.status != 200) {
		            opt.onFail.apply(me, {'xhrState': xhr.readyState, 'xhrStatus':xhr.status});
		            return false;
		        }
		    };

			xhr.send(formData);
		};
	};
})($);