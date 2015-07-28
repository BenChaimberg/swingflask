$(document).ready(function(){
  if ($(window).width() <= 1024) {
    $(window).resize(function(){
      $("iframe").css({"height":.75*$(window).width()-10});
      $("iframe").css({"width":$(window).width()-10});
    });
    $(".label").click(function(){
      $("iframe").css({"height":.75*$(window).width()-10});
      $("iframe").css({"width":$(window).width()-10});
      $(this).siblings().not(".label").not($(this).next()).slideUp("slow");
      $(this).next().slideToggle("slow",function(){
        $('html, body').animate({scrollTop:$(this).prev().offset().top-71},500,function(){
          $("#buyreturn").hide("fast");
          $(".buystuff").hide("fast",function(){
            $(".purchase p").not("#buyreturn").show("fast");
          });
        });
        });
      $(this).siblings().removeClass("open");
      $(this).toggleClass("open");
    });
  }
  if ($(window).width() > 1024) {
    $(".stuff").insertAfter($("#tabs").children().last());
    $(".label").click(function(event){
      event.preventDefault();
      $(this).removeClass("label");
      var labelclass = $(this).attr("class")
      $(this).addClass("label");
      labelclass = "." + labelclass
      if ($(labelclass).not(".label").css("display") == "none") {
        $(this).prev().css({"border-right":"1px solid black"});
        $(this).next().not(".stuff").css({"border-left":"1px solid black"});
        $(this).css({"border-left":"0px solid black"});
        $(this).css({"border-right":"0px solid black"});
        $(this).css({"border-bottom":"0px solid black"});
        $(this).hover(function(){$(this).css({"background-color":"#FFFFFF"})},function(){$(this).css({"background-color":"#FFFFFF"})});
        $(labelclass).not(".label").css({"display":"block"})
      }
      $(this).css({"background-color":"#FFFFFF"})
      $(this).siblings().not(labelclass).not(".label").css({"display":"none"});
      $(this).siblings().not(labelclass).not(".stuff").css({"border-bottom":"1px solid black"});
      $(".label:nth-last-of-type(1)").css({"border-right":"1px solid black"});
      $(".label:nth-of-type(1)").css({"border-left":"1px solid black"});
      $(this).siblings().not(labelclass).not(".stuff").css({"background-color":"#eee"});
      $(this).siblings().not(labelclass).not(".stuff").hover(function(){$(this).css({"background-color":"#CCFFCC"})},function(){$(this).css({"background-color":"#eee"})});
      $("#buyreturn").hide("fast");
      $(".buystuff").hide("fast",function(){
        $(".purchase p").not("#buyreturn").show("fast");
      });
    });
  }
  $("#buyreturn").click(function(event){
    $("#buyreturn").hide("fast");
    $(".buystuff").hide("fast",function(){
      $(".purchase p").not("#buyreturn").show("fast");
    });
  });
  $(".buybutt").click(function(event){
    event.preventDefault();
    $('html, body').stop();
    var clicked = $(".buybutt").index(this);
    $(".purchase p").hide("fast",function(){
      $("#buyreturn").show("fast")
      $($(".buystuff").get(clicked)).show("fast");
    });
  });
});
