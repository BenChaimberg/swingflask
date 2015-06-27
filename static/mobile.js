$(document).ready(function(){
	if ($(window).width() <= 1024) {
		$("#links").insertBefore("#footer");
		$("#div-search").insertBefore("#sidebar-before");
		$("#category-list").prepend("<li>"+$("#category-heading").html()+"</li>");
		$("#brand-list").prepend("<li>"+$("#brand-heading").html()+"</li>");
		$("#mobile-header-left").click(function(){
			var currentPosition = $(document).scrollTop();
			$("#sidebar").animate({ marginLeft: "0%"} , 500);
			$("#sidebar").css({"-webkit-overflow-scrolling": "touch"});
			$("body").css({"overflow":"hidden"});
			$("body").css({"position":"fixed"});
			$("body").css({"width":$(window).width()});
		});
		$("#mobile-header-center").click(function(){
			$('html, body').animate({scrollTop:0});
		});
		$("#sidebar-before").click(function(){
			$("#sidebar").animate({ marginLeft: "-100%"} , 500);
			$("#sidebar").css({"-webkit-overflow-scrolling": "auto"});
			$("body").css({"overflow":"default"});
			$("body").css({"position":"default"});
			$('html, body').animate({scrollTop:currentPosition});
		});
		$(window).resize(function(){
			facebookWidthResize();
		});
	}
});
$(window).load(function(){
	facebookWidthResize();
});
var facebookWidthResize = function(){
	console.log('resize');
	$(document).find('div.fb-post').each(function() {
		$(this).attr('data-width', $(this).parent().width());
	});
	$(document).find('div.fb-page').each(function() {
		$(this).attr('data-width', $(this).parent().width());
		$(this).attr('data-height', $(window).height()-125);
	});
	if (FB) {
		FB.XFBML.parse();
	}
}
