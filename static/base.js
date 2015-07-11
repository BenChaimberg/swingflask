$(document).ready(function(){
	var windowWidth = $(window).width();
	var currentPosition;
	var moveWidth;
	if ($(window).width() <= 1024) {
		$("#links").insertBefore("#footer");
		$("#div-search").insertBefore("#category-heading");
		$("#category-list").prepend("<li>"+$("#category-heading").html()+"</li>");
		$("#brand-list").prepend("<li>"+$("#brand-heading").html()+"</li>");
		$("#mobile-header-left").click(function(){
			moveWidth = ($("#content").width() * .75);
			currentPosition = $(document).scrollTop();
			$("#mainright").offset({top:-currentPosition+$("#mobile-header").height()+5});
			$("#back-handle").width("100%");
			$("#back-handle").animate({left: 0} , 500);
			$("#sidebar").animate({ left: 0} , 500,function(){
				$("#sidebar").css({"-webkit-overflow-scrolling": "touch"});
			});
			$("#mainright").css({"position":"fixed"});
			$("#mainright").animate({ left: moveWidth } , 500);
			$("#mobile-header").animate({ left: moveWidth } , 500);
			$("body").css({"width":$(window).width()});
			$("#mainright").css({"width":"100%"});
		});
		$("#mobile-header-center").click(function(){
			$('html, body').animate({scrollTop:0});
		});
		$("#back-handle").click(function(event){
			if ($("#mainright").offset().left != 0) {
				event.preventDefault();
				$("#back-handle").animate({left:-moveWidth}, 500,function(){
					$("#back-handle").css({"width":"75%"});
				});
				$("#sidebar").animate({ left: -moveWidth} , 500,function(){
					$("#sidebar").css({"-webkit-overflow-scrolling": "auto"});
				});
				$("#mainright").animate({ left: 0} , 500,function(){
					$("#mainright").css({"position":"default"});
					$('html, body').scrollTop(currentPosition);
				});
				$("#mobile-header").animate({ left: 0} , 500);
			}
		});
		$(window).resize(function(){
			facebookWidthResize();
			moveWidth = ($(window).width() * .75);
			console.log(moveWidth);
			$("#content, #mainright, html, body").width($(window).width());
			$("#back-handle").offset({left:-moveWidth});
			$("#back-handle").css({"width":"75%"});
			$("#sidebar").css({"width":"75%"});
			$("#sidebar").offset({ left: -moveWidth});
			$("#sidebar").css({"-webkit-overflow-scrolling": "auto"});
			$("#mainright").offset({ left: 0});
			$("#mainright").css({"position":"default"});
			$("#mobile-header").width("100%");
			$("#mobile-header").offset({ left: 0} , 500);
		});
	}
});
$(window).load(function(){
	facebookWidthResize();
});
var facebookWidthResize = function(){
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
