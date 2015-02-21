$(document).ready(function(){
	if ($(window).width() <= 1024) {
		$("#links").insertBefore("#footer");
		$("#mobile-header-left").click(function(){
			$("#sidebar").animate({ marginLeft: "0%"} , 500);
			$("body").css({"overflow":"hidden"});
			$("body").css({"position":"fixed"});
			$("body").css({"width":$(window).width()});
		});
		$("#mobile-header-center").click(function(){
			$('html, body').animate({scrollTop:0});
		});
		$("#sidebar-before").click(function(){
			$("#sidebar").animate({ marginLeft: "-100%"} , 500);
			$("body").css({"overflow":"default"});
			$("body").css({"position":"default"});
		});
		$(window).resize(function(){
			$(document).find('div.fb-post').each(function() {
				$(this).attr('data-width', $(this).parent().width());
			});
			if (FB) {
				FB.XFBML.parse();
			}
		});
	}
});
