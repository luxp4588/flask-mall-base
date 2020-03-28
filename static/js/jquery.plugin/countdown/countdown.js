(function($){
	$.fn.countDown = function(secs) {
		secs = parseInt(secs);
		var timeId,
			me = $(this),
			HMSObj,
			HMSHtml = '<span class="col-md-1"><span class="time-border">#HH#</span></span>' +
            '<span class="col-md-1">：</span>' +
            '<span class="col-md-1"><span class="time-border">#MM#</span></span>' +
            '<span class="col-md-1">：</span>' +
            '<span class="col-md-1"><span class="time-border">#SS#</span></span>';
		var timeId = setInterval(function(){
			HMSObj = $.secsToHMS(secs);
			me.html(HMSHtml.replace('#HH#', HMSObj.H).replace('#MM#', HMSObj.M).replace('#SS#', HMSObj.S));
			secs--;
			if(secs < 0) {
				clearInterval(timeId);
			}
		}, 1000);

	};
	$.extend({
		secsToHMS : function(secs) {
			var H = '00',
				M = '00',
				S = '00';
			H = $.formatTimeDouble(parseInt(secs/3600));
			secs %= 3600;
			M = $.formatTimeDouble(parseInt(secs/60));
			secs %= 60;
			S = $.formatTimeDouble(parseInt(secs));
			return {
				H : H,
				M : M,
				S : S
			}
		},
		formatTimeDouble: function(time) {
			return 10 <= time ? time : 
					time > 0 ? '0' + time : '00';
		}
	});
})($);
