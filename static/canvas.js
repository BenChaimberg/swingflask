var resizings = function(){
	$("#canvas").offset({ top: $("#sidebar").offset().top, left:$("#sidebar").offset().left+$("#sidebar").width()+15 });
}
$(window).resize(function(){
	resizings();
});
$(window).load(function(){
	resizings();
});
$(document).ready(function(){
	$(document).find('div.fb-post').each(function() {
		$(this).attr('data-width', $(this).parent().width());
	});
	resizings();
	var ctx = $("#canvas").get(0).getContext('2d');
	ctx.scale(2, 2);
	ctx.strokeStyle = "grey";
	ctx.fillStyle = "black";
	times = 6;
	startx = 10;
	starty = 18;
	for (i=1;i<=times;i++){
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
});
