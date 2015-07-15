$(window).load(function(){
	var hsl;
	var hsls = [];
	var tds = document.getElementById('category-table-desktop');
	var imgs = tds.getElementsByTagName('img');
	for (i = 0; i < imgs.length; i++) {
		try {
			var rgb = getAverageColor(imgs[i]);
			hsl = rgbToHsl(rgb.r,rgb.g,rgb.b);
		}
		catch(err) {
			hsl = {h:1/12,s:1,l:.2};
		}
		hsls.push(hsl);
	}
	$('.product-overlay').mouseover(function(){
		$(this).finish();
		index = $(this).parent().index()+3*$(this).parent().parent().index();
		$(this).css({'background-color':'hsl(' + Math.round(hsls[index].h * 360) + ', ' + Math.round(hsls[index].s * 100) + '%, ' + Math.round(hsls[index].l * 100) + '%)'});
		if (hsls[index].l < .75) {
			$(this).css({'color':'white'});
		}
		else {
			$(this).css({'color':'black'});
		}
		$(this).animate({opacity: .9}, 300);
	});
	$('.product-overlay').mouseout(function(){
		$(this).finish();
		$(this).animate({opacity: 0}, 300,function(){
			$(this).css({'background-color':'transparent'});
			$(this).css({'color':'transparent'});
		});
	});
});
