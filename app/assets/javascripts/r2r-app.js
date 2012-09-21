$(document).ready(function() {

	var show_application = function(){
		$("#information").hide();
		$("#application").show();
		window.scrollTo(0,500);
		window.location.hash = '#application';
	}
	
	var hide_application = function(){
	    $("#application").hide();
		$("#information").show();
		window.location.hash = '';
	}

	$("#application").hide(); 

	$(".Apply .button").live( 'click', function() {
		show_application();
		
		//Firefox for some reason does not refresh the DOM in iFrame
	    if($.browser.mozilla){
			document.getElementsByTagName('iframe')[0].src=document.getElementsByTagName('iframe')[0].src
	    }

	});

    $("div#application a.back").click(function() {
		hide_application();
	});

	$("a#reg").click( function() {
	   show_application();
	});
		
	// anchor scrolling
	var didScroll = true;

	var sections = $(".wrapper").each(function(index) {
		$(this).data("height", $(this).height());
	});
	var links = $(".subnav a");

	$(".subnav").localScroll({
		axis : "y",
		duration : 1000,
		easing : "easeInOutExpo",
		hash : true
	});	
		
	if(window.location.hash == '#application'){
		show_application();
	}

});;
