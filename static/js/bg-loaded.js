/*
 * BG Loaded
 * 
 *
 * Copyright (c) 2014 Jonathan Catmull
 * Licensed under the MIT license.
 */
 
 (function($){
 	$.fn.bgLoaded = function(custom) {

 		var self = this;

	// Default plugin settings
	var defaults = {
		afterLoaded : function(){
			this.addClass('bg-loaded');
		}
	};

		// Merge default and user settings
		var settings = $.extend({}, defaults, custom);

		// Loop through element
		self.each(function(){
			var $this = $(this),
				bgImgs = $this.css('background-image').split(', ');
			$this.data('loaded-count',0);

			$.each( bgImgs, function(key, value){
				var img = value.replace(/^url\(["']?/, '').replace(/["']?\)$/, '');
				$('<img/>').attr('src', img).load(function() {
					$(this).remove(); // prevent memory leaks
					$this.data('loaded-count',$this.data('loaded-count')+1);
					if ($this.data('loaded-count') >= bgImgs.length) {
						settings.afterLoaded.call($this);
					}
				});
			});

		});
	};
})(jQuery);