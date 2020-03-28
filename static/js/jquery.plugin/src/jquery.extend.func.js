(function($) {
	$.extend({
		strReplace: function(str, repMap) {
			for(var i in repMap) {
				str = str.replace(i, repMap[i]);
			}
			return str;
		},
	});
})($);