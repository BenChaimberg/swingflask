var resizings = function(){
	$("#canvas").offset({ top: $("#sidebar").offset().top, left:$("#sidebar").offset().left+$("#sidebar").width()+15 });
	if ($(window).width() >= 1024) {	var sidebarOffset = $("#sidebar").offset().top;
		var contentOffset = $("#content").offset().top;
		var sidebarHeight = $("#sidebar").height();
		var contentPaddingTop = parseInt($("#content").css('padding-top').replace("px", ""));
		var contentPaddingBottom = parseInt($("#content").css('padding-bottom').replace("px", ""));
		var sidebarPaddingTop = parseInt($("#sidebar").css('padding-top').replace("px", ""));
		var sidebarPaddingBottom = parseInt($("#sidebar").css('padding-bottom').replace("px", ""));
		var contentMinHeight = sidebarHeight+sidebarOffset-contentOffset+sidebarPaddingTop+sidebarPaddingBottom-contentPaddingTop-contentPaddingBottom;
		$("#content").css({'min-height':contentMinHeight+'px'});
	}
}
$(window).resize(function(){
	resizings();
});
$(window).load(function(){
	resizings();
});
var canvassing = function(){
	resizings();
	var ctx = $("#canvas").get(0).getContext('2d');
	ctx.scale(2, 2);
	ctx.strokeStyle = "grey";
	ctx.fillStyle = "black";
	var startx = 10;
	var starty = 19;
	times = ($("#sidebar").height()-5)/(2*starty);
	for (i=1;i<times;i++){
		ctx.beginPath();
		ctx.moveTo(startx, starty*i-2);
		ctx.lineTo(startx+30, starty*i+1);
		ctx.stroke();

		ctx.beginPath();
		ctx.moveTo(startx, starty*i+2);
		ctx.lineTo(startx+30, starty*i+5);
		ctx.stroke();

		ctx.beginPath();
		ctx.arc(startx,starty*i,4,0,2*Math.PI);
		ctx.fill();

		ctx.beginPath();
		ctx.arc(startx+30,starty*i+3,4,0,2*Math.PI);
		ctx.fill();
	}
}
